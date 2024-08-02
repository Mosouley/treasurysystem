import { PaymentMode } from './invoice';
import { BaseEntity } from './base-entity';
export class CashBalance {
    constructor(
                 public id ?: number,
                 public dateHisto?: Date,
                 public payMode?: PaymentMode,
                 public balance ?: number
    ) {}
 }
