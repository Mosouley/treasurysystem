import { BaseEntity } from './base-entity';
import { TransactionLine } from './transactionLine';
export class ProdBalance {
    constructor(
                 public id ?: number,
                 public dateHisto?: Date,
                 public codeProd?: string,
                 public balance ?: number
    ) {}
 }
