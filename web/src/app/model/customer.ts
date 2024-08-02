import { BaseEntity } from "./base-entity";

export class Customer {
    constructor(
                 public id ?: number,
                 public cif ?: number,
                 public name?: string,
                 public user?: BaseEntity,
                 public email?: string,
                 public segment?:BaseEntity,
                 public active?: boolean,
                 public customerMandate?: BaseEntity
    ) {}
 }
