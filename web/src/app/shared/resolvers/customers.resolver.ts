import { CustomerService } from '../services/customer.service';
import {Injectable} from '@angular/core';

@Injectable()
export class CustomerResolver  {

  constructor(private cust_service: CustomerService) {
  }

  resolve() {
    return this.cust_service.listAll();
  }
}
