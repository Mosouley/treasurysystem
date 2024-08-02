import { BaseEntity } from './base-entity';

export class Product {

  constructor(
               public productId?: number,
                public name?: string,
                public prodClass?: BaseEntity,
  ) {}

}
