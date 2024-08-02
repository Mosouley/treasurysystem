import { Currency } from './currency';
import { Product } from './product';

import { Customer } from './customer';
import { Dealer } from './dealer';


export enum BuySell {
  Buy,
  Sell
}

export enum Status {
  Amended,
  Verified,
  Matured,
  Cancelled
}
export interface TradeStatus {
  value: string;
  label: string;
}

export interface Trade {
      id: number,
     trade_id: number;
     tx_date: Date;
     val_date: Date;
     ccy1: Currency;
     ccy2: Currency;
     buy_sell: BuySell;
     amount1: number ;
     amount2: number;
     deal_rate: number;
     fees_rate: number;
     system_rate: number;
     deal_pnl: number;
     tx_comments: string;
     customer: Customer;
     product: Product;
     trader: Dealer;
     status: TradeStatus;
     last_updated: Date
  }





