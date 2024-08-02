import { BaseEntity } from './base-entity';
import { TransactionLine } from './transactionLine';

export const enum InvoiceStatus {
  CANCELLED,
  PAYE,
  NONPAYE
}
export enum PaymentMode {
  CASH,
  BANK,
  MOBILE,
  CREDIT
}
export class Invoice {

  constructor(
    public id?: number,
    public invoiceRef?: any,
    public totalInvoice?: number,
    public dateTrans?: Date,
    public statut?: InvoiceStatus,
    public paymentMode?: PaymentMode,
    public client?: BaseEntity,
    public transactionLines?: TransactionLine[],
    public user?: BaseEntity ) {}
  }



