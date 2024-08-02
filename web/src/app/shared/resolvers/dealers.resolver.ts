import {Injectable} from '@angular/core';


import { DealerService } from '../services/dealer.service';



@Injectable()
export class DealersResolver  {

  constructor(private curr_service: DealerService) {
  }

  resolve() {
    // this.curr_service.list().subscribe(x => {
    //   console.log(x);
    // });
    return this.curr_service.listAll();
  }
}
