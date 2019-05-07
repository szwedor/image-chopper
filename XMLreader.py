
import xmltodict
import pandas as pd
import os
import glob

class XMLreader():
    def _list_assurer(self,d):
        if type(d) == list:
            return d
        return [d]
    def _flatten_dict(self, df, column):
        size = df[column].apply(pd.Series)
        return pd.concat([df, size], axis=1).drop(column, axis=1)
    def _flatten_list_dict(self, df, column):
        tmp = df[column].apply(self._list_assurer).apply(pd.Series)
        tmp = tmp.transpose().iloc[:,0]
        tmp = tmp.apply(pd.Series)
        return (
            df.drop(column,axis=1).assign(key=1)
            .merge(tmp.assign(key=1), on="key")
            .drop("key", axis=1)
        )
    def read_config(self,path):
        with open(path, 'r') as f:
            xml = f.read()
        xmlDict = xmltodict.parse(xml)
        df = pd.DataFrame.from_dict(xmlDict, orient = 'index')
        df = self._flatten_dict(df,'size')
        df = self._flatten_list_dict(df,'object')
        df = self._flatten_dict(df,'bndbox')
        return df.reset_index()
    def read_configs(self, path, pattern):
        search_path = os.path.join(path,pattern)
        return pd.concat([self.read_config(path) for path in glob.glob(search_path)]).reset_index()
            
