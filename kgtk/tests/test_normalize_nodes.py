import shutil
import unittest
import tempfile
import pandas as pd
from kgtk.cli_entry import cli_entry
from kgtk.exceptions import KGTKException


class TestKGTKNormalizeNodes(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = 'data/sample_kgtk_nodes.tsv'
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_kgtk_normalize_nodes_default(self):
        cli_entry("kgtk", "normalize-nodes", "-i", self.file_path, "-o", f'{self.temp_dir}/normalize.tsv')
        cli_entry("kgtk", "normalize-nodes", "-i", self.file_path, "-o", '/tmp/normalize.tsv')

        df = pd.read_csv(f'{self.temp_dir}/normalize.tsv', sep='\t')

        self.assertEqual(len(df), 52)
        df = df.loc[df['node1'] == 'Q183'].loc[df['label'] == 'label']
        self.assertTrue(len(df), 3)
        print(df)
        labels = list(df['node2'].unique())
        
        self.assertTrue("'Germany'@en" in labels)
        self.assertTrue("'Германия'@ru" in labels)
        self.assertTrue("'Німеччина'@uk" in labels)
