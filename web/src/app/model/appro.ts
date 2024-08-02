import { BaseEntity } from './base-entity';
import { TransactionLine } from './transactionLine';
export class Appro {
    constructor(
                 public id ?: number,
                 public approRef?: string,
                 public transactionLines?: TransactionLine[],
                 public user?: BaseEntity,
                 public dateAppro ?: Date
    ) {}
 }
