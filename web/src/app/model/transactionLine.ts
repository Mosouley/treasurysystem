import { BaseEntity } from './base-entity';


export class TransactionLine {

    public id!: number;
    public debitAmount!: number ;
    public creditAmount!: number;
    public quantity!: number;
    public unitValue!: number;
    public produit!: BaseEntity;
    public invoice!: BaseEntity;
    public txDate!: Date;
  }



