import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { NgFor } from '@angular/common';
import { MatTableModule } from '@angular/material/table';

@Component({
    selector: 'app-data-table',
    templateUrl: './data-table.component.html',
    styleUrls: ['./data-table.component.css'],
    standalone: true,
    imports: [MatTableModule, NgFor]
})
export class DataTableComponent implements  OnChanges{

  @Input()
  data!: any[];
  displayedColumns: string[] = [];
  dataSource: any[] = [];
  ngOnChanges(changes: SimpleChanges): void {
    // if (changes['data']) {
    //   // Extract headers from first row of data
    //   this.displayedColumns = this.data[0];
    //   console.log(this.transposeData(this.data));

    //   // Remove headers from data
    //   this.dataSource = this.data.slice(1);
    // }

    if (changes['data']) {
      // Transpose data and add headers to first column

       const transposedData = this.transposeData(this.data);
      const headers = transposedData[0] //this.data[0]   //

      this.displayedColumns = [ ...headers];
      this.dataSource = transposedData.slice(1) //this.data.slice(1)
        //
  }
  }


  transposeData(data: any[][]): any[][] {
    // Get the number of rows and columns in the input data
    console.log(data);

    const numRows = data.length;
    const numCols = data[0].length;

    // Create an array to hold the transposed data
    const transposedData = new Array(numCols);

    // Iterate over the rows and columns of the input data
    for (let i = 0; i < numCols; i++) {
      transposedData[i] = new Array(numRows);
      for (let j = 0; j < numRows; j++) {
        transposedData[i][j] = data[j][i];
      }
    }

    return transposedData;
  }


}
