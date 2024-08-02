import { CurrenciesService } from './../services/currencies.service';
import { Injectable } from '@angular/core';

@Injectable()
export class CurrenciesResolver  {
  constructor(private curr_service: CurrenciesService) {}

  resolve( ) {
    return this.curr_service.listAll();
      }
  }

