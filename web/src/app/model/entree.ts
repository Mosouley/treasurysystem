import { BaseEntity } from './base-entity';
export class Entree {
    constructor(
                 public id ?: number,
                 public produit?: BaseEntity,
                 public quantite ?: number,
                 public coutEntree?: number,
                 public date ?: Date
    ) {}
 }
