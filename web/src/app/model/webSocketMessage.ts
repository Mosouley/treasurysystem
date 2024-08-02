 export interface webSocketMessage{
    action:string; // action to perform
    data: any // the data to send
}


interface PaginatedData {
  count: number;
  next: string;
  previous: string;
  results: any[];
}
