import {Injectable} from '@angular/core';


import { ProductService } from '../services/product.service';



@Injectable()
export class ProductsResolver  {

  constructor(private prod_service: ProductService) {
  }

  resolve() {
    // this.prod_service.list().subscribe(x => {
    //   console.log(x);
    // });
    return this.prod_service.listAll();
  }
}
