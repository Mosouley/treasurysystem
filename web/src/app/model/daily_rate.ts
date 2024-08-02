import { Currency } from "./currency";

export class DailyRate {
    constructor(
      public id : number,
      public date: Date,
      public rateLcy: number,
      public last_update : Date,
      public ccy : Currency,

    ) {}
 }

 export interface ApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: any[]; // Adjust this based on your actual data structure
}


export interface Card {
  imgSrc: string;
  name: string;
  description: string}
