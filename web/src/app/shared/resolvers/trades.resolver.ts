import {Injectable} from '@angular/core';
import { TradeService } from '../services/trade.service';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { Trade } from '../../model/trade';



@Injectable()
export class TradesResolver  {

  constructor(private trades_service: TradeService) {
  }

  resolve(route: ActivatedRouteSnapshot): Observable<Trade[]> {
      // Get the 'pageSize' parameter from the route or set a default value
      // const limit = 40 //route.queryParams['limit'];
      const offset = 30 // route.queryParams['offset'];

    // return this.trades_service.list(40, 40);
    return this.trades_service.fetchData(offset)
  }
}
