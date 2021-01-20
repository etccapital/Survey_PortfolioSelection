class CRP(Strategy):
    def __init__(self, port):
        if not hp.isvalidport(port): raise Exception("Not a valid portfolio!")
        self.port = np.array(port)
    def run(self, df:pd.DataFrame):
        #note that directly multiplying np arrays with "*" will produce incorrect results
        rel_rets = np.matmul(df.to_numpy(), self.port).transpose()
        ts_daily_rets = pd.Series(index=df.index, data=rel_rets)
        return OLPSResult(ts_daily_rets)
    def name(self):
        return "Constant Rebalanced Portfolio"
