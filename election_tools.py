"""Geprüfte Datenaufbereitung für die explorativen Wahl-Notebooks."""

import re

import geopandas as gpd
import numpy as np
import pandas as pd


def load_votes(path):
    """Alle Gebietsebenen einlesen; LAND nicht durch skiprows verlieren."""
    data = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
    for col in data.columns:
        if re.fullmatch(r"[DF]\d+", col) or col in (
            "Erststimmen gueltige (D)", "Zweitstimmen gueltige (F)",
            "Erststimmen ungueltige (C)", "Zweitstimmen ungueltige (E)",
            "Waehler gesamt (B)", "gemeldete Wahlbezirke", "Anzahl Wahlbezirke",
        ):
            data[col] = pd.to_numeric(data[col], errors="raise")
    return data


def municipal_votes(raw):
    """Nur Gemeindezeilen plus fehlende Großstädte aus deren Wahlkreisen.

    Freiburgs Gemeinde-Teilzeilen werden nach AGS summiert. Gemeinsame
    Briefwahlbezirke werden nicht künstlich auf einzelne Gemeinden verteilt.
    """
    vote_columns = [c for c in raw if re.fullmatch(r"[DF]\d+", c)]
    count_columns = vote_columns + ["Erststimmen gueltige (D)", "Zweitstimmen gueltige (F)"]
    municipalities = raw.loc[raw.Gebietsart.eq("GEMEINDE")].copy()
    for ags in ("08111000", "08212000", "08222000"):
        if not municipalities.AGS.eq(ags).any():
            rows = raw.loc[raw.Gebietsart.eq("WAHLKREIS") & raw.AGS.eq(ags)]
            if rows.empty:
                raise ValueError(f"Fehlende Gemeinde und Wahlkreise für {ags}")
            municipalities = pd.concat([municipalities, rows], ignore_index=True)
    if municipalities.AGS.isna().any() or not municipalities.AGS.str.fullmatch(r"08\d{6}").all():
        raise ValueError("Ungültiger Gemeindeschlüssel in den Gemeindeergebnissen")
    if municipalities.duplicated(["Gebietsart", "Gebietsnummer"]).any():
        raise ValueError("Doppelte Gebietseinträge")
    counts = municipalities.groupby("AGS")[count_columns].sum(min_count=1)
    names = municipalities.groupby("AGS").Gemeindename.first()
    result = counts.join(names).reset_index()
    for prefix, denominator in (("D", "Erststimmen gueltige (D)"), ("F", "Zweitstimmen gueltige (F)")):
        cols = [c for c in vote_columns if c.startswith(prefix)]
        if not np.allclose(result[cols].fillna(0).sum(axis=1), result[denominator]):
            raise ValueError(f"Parteistimmen ergeben nicht die gültigen Stimmen ({prefix}).")
        if (result[denominator] <= 0).any():
            raise ValueError("Gemeinde ohne gültige Stimmen")
    return result


def balance_table(raw, municipalities):
    columns = ["Erststimmen gueltige (D)", "Zweitstimmen gueltige (F)"]
    land = raw.loc[raw.Gebietsart.eq("LAND"), columns].sum()
    districts = raw.loc[raw.Gebietsart.eq("WAHLKREIS"), columns].sum()
    precincts = raw.loc[raw.Gebietsart.isin(["URNENWAHLBEZIRK", "BRIEFWAHLBEZIRK"]), columns].sum()
    if not np.array_equal(land, districts) or not np.array_equal(land, precincts):
        raise ValueError("Land, Wahlkreise und Wahlbezirke stimmen nicht überein.")
    municipal_sum = municipalities[columns].sum()
    return pd.DataFrame({"Land": land, "Wahlkreise": districts, "Wahlbezirke": precincts,
                         "Gemeinden": municipal_sum, "nicht_gemeindescharf": land - municipal_sum}).T


def add_shares(municipalities, rename_map):
    frame = municipalities.rename(columns=rename_map).copy()
    for kind, denominator in (("EST", "erststimmen_gueltig"), ("ZST", "zweitstimmen_gueltig")):
        cols = [c for c in frame if c.endswith("_" + kind)]
        for col in cols:
            # Nicht angetretene Parteien bleiben bei Erststimmen fehlend.
            frame[col + "_p"] = frame[col] / frame[denominator]
    frame["R"] = frame.CDU_ZST / frame.GRUENE_ZST.where(frame.GRUENE_ZST > 0)
    frame["R_log"] = np.log(frame.R.where(frame.R > 0))
    cols = [c for c in frame if c.endswith("_ZST")]
    votes = frame[cols].fillna(0)
    frame["winner_ZST"] = votes.idxmax(axis=1).str.removesuffix("_ZST")
    ties = votes.eq(votes.max(axis=1), axis=0).sum(axis=1) > 1
    frame.loc[ties, "winner_ZST"] = "Gleichstand"
    return frame


def quartiles(series):
    edges = series.dropna().quantile([.25, .5, .75]).to_numpy()
    if len(edges) != 3 or not np.isfinite(edges).all():
        raise ValueError("Keine gültigen Quartilgrenzen")
    values = np.searchsorted(edges, series.to_numpy(), side="left").astype(float)
    values[series.isna()] = np.nan
    return pd.Series(values, index=series.index)


def fdr_bh(p_values, alpha=.05):
    """Benjamini-Hochberg; fehlende p-Werte werden nicht getestet."""
    p = np.asarray(p_values, float)
    valid = np.isfinite(p)
    result = np.zeros(p.shape, bool)
    indices = np.flatnonzero(valid)
    order = indices[np.argsort(p[valid])]
    passed = p[order] <= alpha * np.arange(1, len(order) + 1) / max(len(order), 1)
    if passed.any():
        result[order[:np.flatnonzero(passed)[-1] + 1]] = True
    return result


def load_geometry(path, layer):
    frame = gpd.read_file(path, layer=layer)
    if frame.crs is None or not frame.crs.is_projected:
        raise ValueError("Projizierte Geometrien mit CRS benötigt")
    if frame.AGS.duplicated().any():
        raise ValueError("Doppelte AGS in der Geometrie")
    return frame


def setup_ternary_axis(ax, major_step=10, **kwargs):
    ticks = np.arange(major_step / 100, 1, major_step / 100)
    for axis in (ax.taxis, ax.laxis, ax.raxis):
        axis.set_ticks(ticks)
        axis.set_ticklabels([f"{v:.0%}" for v in ticks] if kwargs.get("show_labels") else [])
    ax.grid(kwargs.get("draw_grid", True), linestyle=":", linewidth=.8)
