import {Injectable} from '@angular/core';


import { SegmentService } from '../services/segment.service';



@Injectable()
export class SegmentsResolver  {

  constructor(private curr_service: SegmentService) {
  }

  resolve() {
    // this.curr_service.list().subscribe(x => {
    //   console.log(x);
    // });
    return this.curr_service.listAll();
  }
}
