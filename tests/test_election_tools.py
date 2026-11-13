import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from election_tools import add_shares, balance_table, fdr_bh, load_votes, municipal_votes, quartiles


class ElectionTests(unittest.TestCase):
    def test_quartile_ties_and_missing(self):
        result = quartiles(pd.Series([1., 1., 1., 1., np.nan]))
        self.assertTrue(result.iloc[:4].eq(0).all())
        self.assertTrue(np.isnan(result.iloc[4]))

    def test_bh_known_example(self):
        np.testing.assert_array_equal(fdr_bh([.001, .01, .04, .8, np.nan]),
                                      [True, True, False, False, False])

    def test_bh_no_discoveries(self):
        self.assertFalse(fdr_bh([.2, .3, np.nan]).any())

    def test_shares_and_tie(self):
        frame = pd.DataFrame({'D1': [10.], 'F1': [5.], 'F2': [5.],
                              'D': [10.], 'F': [10.]})
        result = add_shares(frame, {'D1': 'GRUENE_EST', 'F1': 'GRUENE_ZST',
                                   'F2': 'CDU_ZST', 'D': 'erststimmen_gueltig',
                                   'F': 'zweitstimmen_gueltig'})
        self.assertEqual(result.loc[0, 'winner_ZST'], 'Gleichstand')
        self.assertEqual(result.loc[0, 'R_log'], 0.)
        self.assertEqual(result.loc[0, 'CDU_ZST_p'], .5)


class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.raw = load_votes(root / 'data/bw2026_snapshot.csv')
        cls.municipalities = municipal_votes(cls.raw)

    def test_aggregation_unique_and_complete(self):
        self.assertEqual(len(self.municipalities), 1101)
        self.assertTrue(self.municipalities.AGS.is_unique)
        self.assertTrue(self.municipalities.AGS.str.len().eq(8).all())

    def test_city_aggregation_does_not_count_overlapping_levels(self):
        result = self.municipalities.set_index('AGS')
        for ags in ['08111000', '08212000', '08222000', '08311000']:
            precincts = self.raw[self.raw.AGS.eq(ags) & self.raw.Gebietsart.isin(['URNENWAHLBEZIRK', 'BRIEFWAHLBEZIRK'])]
            self.assertEqual(result.loc[ags, 'Zweitstimmen gueltige (F)'],
                             precincts['Zweitstimmen gueltige (F)'].sum())

    def test_state_balance_and_unassigned_mail_votes(self):
        balance = balance_table(self.raw, self.municipalities)
        mail = self.raw[self.raw.AGS.eq('BW')]
        for col in ['Erststimmen gueltige (D)', 'Zweitstimmen gueltige (F)']:
            self.assertEqual(balance.loc['nicht_gemeindescharf', col], mail[col].sum())

    def test_duplicate_geographies_rejected(self):
        row = self.raw[self.raw.Gebietsart.eq('GEMEINDE')].iloc[[0]]
        with self.assertRaisesRegex(ValueError, 'Doppelte'):
            municipal_votes(pd.concat([self.raw, row], ignore_index=True))


if __name__ == '__main__':
    unittest.main()
