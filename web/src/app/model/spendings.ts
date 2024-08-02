import { BaseEntity } from './base-entity';


export enum TypeSpending {
  CHARGES_PERSONNEL,
  LOYER_LOCATIONS,
  TRANSPORT,
  CHARGES_ELECTRICITE,
  CHARGES_EAU

}

export class Spending {
    constructor(
                 public id ?: number,
                 public dateSpending ?: Date,
                 public typeSpending?: TypeSpending,
                 public valueSpending ?: number,
                 public commentSpending?: string

    ) {}
 }
