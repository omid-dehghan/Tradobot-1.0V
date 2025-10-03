import datetime
import csv
import os

class Announcer:

    logs = {
        "infos": 0,
        "warns": 0,
        "errors": 0,
        "logs": 0,
        "signals": 0,
        "trade": {"limit": 0,
                  "status": 0,
                  "delete": 0}}
    
    announcer_lid = 0
    announcer_num = 1
    snapshot_num = 0

    def __init__(self, info_print:bool = True, error_print:bool = True, log_print:bool = True, save_logs: bool = False, save_trades: bool = False, save_snapshots: bool = True, logs_file_name: str = "logs.csv", trade_file_name:str = "trades.csv", snapshots_file_name = "snapshots.csv"):
        self.log_print = log_print
        self.error_print = error_print
        self.info_print = info_print
        self.save_logs = save_logs
        self.save_trades = save_trades
        self.save_snapshots = save_snapshots
        self.logs_file_name = logs_file_name
        self.trades_file_name = trade_file_name
        self.snapshot_file_name = snapshots_file_name
        
        if self.save_logs and not os.path.exists(self.logs_file_name):
            with open(self.logs_file_name, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["LID", "number","timestamp", "level", "message"])
        
        if self.save_trades and not os.path.exists(self.trades_file_name):
            with open(self.trades_file_name, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["LID", "number","timestamp", "level", "message"])
        
        if self.save_snapshots and not os.path.exists(self.snapshot_file_name):
            with open(self.snapshot_file_name, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["number","date", "time", "symbol", "sell_price", "buy_price", "profit/loss"])

    def _write(self, id, level: str, message: str):
        
        if id == 600 or id == 700 or id == 800:
            self.announcer_lid = f"{id}{self.logs['trade'][level]}"
        else:
            self.announcer_lid = f"{id}{self.logs[level.lower() + 's']}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{self.announcer_lid}] [{self.announcer_num}] [{timestamp}] [{level}] {message}"
        
        if (level == "LOG" and self.log_print) or (level == "INFO" and self.info_print) or (level == "ERROR" and self.error_print) or level == "WARN" or level == "SIGNAL":
            self.announcer_num += 1
            print(formatted)


        if self.save_logs:
            with open(self.logs_file_name, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([self.announcer_lid, self.announcer_num, timestamp, level, message])

        if self.save_trades and (id == 600 or id == 700 or id == 800):
            with open(self.trades_file_name, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([self.announcer_lid, self.announcer_num, timestamp, level, message])

    def _write_snapshots(self, symbol, sellprice, buyprice, profitloss):
        self.snapshot_num += 1
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        if self.save_snapshots:
            with open(self.snapshot_file_name, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([self.snapshot_num, date, time, symbol, sellprice, buyprice, profitloss])

    def info(self, message: str):
        self.logs['infos'] += 1
        self._write(100, "INFO", message)

    def warn(self, message: str):
        self.logs['warns'] += 1
        self._write(200, "WARN", message)

    def error(self, message: str):
        self.logs['errors'] += 1
        self._write(300, "ERROR", message)

    def log(self, message: str):
        self.logs['logs'] += 1
        self._write(400, "LOG", message)

    def signal(self, message: str):
        self.logs['signals'] += 1
        self._write(500, "SIGNAL", message)
    
    def trade(self, level, message:str):
        if level == "limit":
            id = 600
        elif level == "status":
            id = 700
        elif level == "delete":
            id = 800
        self.logs['trade'][level] += 1
        self._write(id, level=level, message=message)

    def mms_position_announce(self, base, quote, b2q_sellprice, b2q_buyprice,b2q_profitloss, q2b_sellprice, q2b_buyprice, q2b_profitloss):
        message = f"""
        symbol\t        sellprice\tbuyprice\tprofit\\loss
        {base}\t\t{b2q_sellprice}\t\t{b2q_buyprice}\t\t{b2q_profitloss}%
        {quote}\t\t{q2b_sellprice}\t\t{q2b_buyprice}\t\t{q2b_profitloss}%"""    
        self.info(message) 
        self._write_snapshots(base, b2q_sellprice, b2q_buyprice, b2q_profitloss)   
        self._write_snapshots(quote, q2b_sellprice, q2b_buyprice, q2b_profitloss)   

    