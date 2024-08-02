import { BaseEntity } from './base-entity';

export class Sortie {
    constructor(
        public id: number,
        public produit: BaseEntity,
        public quantite: number,
        public prixvente: number,
        public date: Date,
        public user: BaseEntity
    ) { }
}
