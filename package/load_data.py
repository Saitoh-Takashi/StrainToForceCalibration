import csv
import re
import pandas as pd
from package import add_logger


class MinMax:
    def __init__(self, min_val, max_val):
        """
        範囲のクラス
        :param min_val: 範囲の開始
        :param max_val: 範囲の終了
        """
        self.min = min_val  # 最小値
        self.max = max_val  # 最大値


def load_original_csv(path):
    """
    CSVの読み込み
    :param path: データのパス
    :return: CSVの全データを含む配列
    """
    with open(path, newline='') as f:
        # CSV読み込み
        reader = csv.reader(f, delimiter=',')  # CSVの読み込み
        org_csv = [row for row in reader]  # 配列に格納

    return org_csv


class CsvData:
    def __init__(self, path, start_end=MinMax(1, None), dt=0):
        """
        CSVデータのクラス
        :param path: データのパス
        :param start_end: データの範囲（行） デフォルト: 先頭行を列名の行として次の行から最後まで
        :param dt: サンプリング周期 [s] デフォルト: 0
        """
        self.org_csv = load_original_csv(path)  # 元のCSVの配列
        self.start_end = start_end  # データの範囲（行）
        self.n = len(self.org_csv) - 1  # データ点数
        self.dt = dt  # サンプリング周期 [s]
        self.columns = []  # 列名リスト
        self.df = []  # データフレーム
        logger.info('CSVファイルを読み込みました．')

    def to_dataframe(self, index=None):
        """
        データフレームに変換
        :param index: インデックスとする列名
        :return: -
        """
        self.columns = self.org_csv[self.start_end.min - 1]  # 列名のリスト
        self.df = pd.DataFrame(self.org_csv[self.start_end.min: self.start_end.max],
                               columns=self.columns,
                               index=index)  # データフレームの設定
        logger.info('CSVデータをデータフレームに変換しました．')


class NRData(CsvData):
    def __init__(self, path):
        """
        NRのCSVファイルを読み込む
        :param path: データのパス
        """
        super().__init__(path)  # クラスの継承，コンストラクタの呼び出し

        # CSVファイルからパラメータの読み込み
        self.n = int(self.org_csv[10][1])  # データ点数
        self.start_end.min = int(self.org_csv[0][1])  # データ開始行
        self.start_end.max = self.n + self.start_end.min  # データ終了行

        if ''.join(re.findall(r'\D', self.org_csv[9][1])) == 'μs':
            self.dt = float(re.sub(r'\D', '', self.org_csv[9][1])) / 1000000
        elif ''.join(re.findall(r'\D', self.org_csv[9][1])) == 'ms':
            self.dt = float(re.sub(r'\D', '', self.org_csv[9][1])) / 1000
        else:
            self.dt = float(re.sub(r'\D', '', self.org_csv[9][1]))

        # データフレームに変換
        self.to_dataframe()

        self.df = self.df.iloc[:,1:].astype(float)


class ADData(CsvData):
    def __init__(self, path):
        """
        Result_counterを読み込む
        :param path: データのパス
        """
        super().__init__(path, start_end=MinMax(3, None))  # クラスの継承，コンストラクタの呼び出し（3行目から開始）
        self.to_dataframe()  # データフレームに変換
        self.dt = float(self.org_csv[3][0])  # サンプリング周期の取得

        # Columns内のファイル名に不都合な文字列を置換
        for i, column in enumerate(self.columns):
            mod_column = column.replace('[', '_').replace(']', '').replace('/', '')
            self.columns[i] = mod_column

        self.df.columns = self.columns  # Columnsを更新


logger = add_logger.root_logger()
