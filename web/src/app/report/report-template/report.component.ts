import {
  Component,
  Input,
  ViewChild,
  AfterViewInit,
  EventEmitter,
  Output,
  SimpleChanges,
  OnChanges,
} from '@angular/core';
import { DataModel } from '../../model/data.model';
import { MatPaginator, MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource, MatTable, MatTableModule } from '@angular/material/table';
import { CommonModule } from '@angular/common';
import { map, tap } from 'rxjs/operators';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../material/material.module';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css'],
  standalone: true,
  imports: [MatTableModule, MatPaginatorModule, ReactiveFormsModule, CommonModule, FormsModule],
})
export class ReportComponent implements AfterViewInit, OnChanges {
  @Input() modelEntity!: DataModel[];

  @Input() report_name = '';
  @Input() receivedData!: any;
  // @Input()dataValues!: any[];
  @Input() dataValues: any[] = [];
  @Input() hasPaginator = false;
  @Input() isLoading = false;
  @Output() nextPage = new EventEmitter<any>();

  displayedColumns!: string[];

  dataSource: MatTableDataSource<any[]> = new MatTableDataSource<any[]>([]);
  noData: any;

  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatTable) table!: MatTable<any>;
  // Modify the input property to update when dataValues changes
  // @Input() set dataValues(values: any[]) {
  //   this.connectDataSource(this.modelEntity, values);
  // }
  @Input() resultsLength = 0;

  constructor() {
    // Initialize MatTableDataSource with an empty array
    this.dataSource = new MatTableDataSource<any[]>([]);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['receivedData'] || changes['modelEntity']) {
    this.connectDataSource(this.modelEntity, this.receivedData);
    }
  }

  public connectDataSource(model: DataModel[], data: any): void {
    this.displayedColumns = model?.map((c) => c.columnName);
    this.dataSource.data = data;
    this.noData = this.dataSource
      .connect()
      .pipe(map((donnee: any) => donnee.length === 0));
    this.doSortAndPaginate();
    this.table?.renderRows();
  }

  // sumField(data: any, field: string | number) {
  //   return data.reduce(
  //     (
  //       acc: any,
  //       obj: { [x: string]: any; hasOwnProperty: (arg0: any) => any }
  //     ) => acc + (obj.hasOwnProperty(field) ? obj[field] : 0),
  //     0
  //   );
  // }

  ngAfterViewInit(): void {
    this.paginator.page
      .pipe(
        tap((event: PageEvent) => {
          this.onPageChange(event);
        })
      )
      .subscribe();
    this.doSortAndPaginate();
  }

  public doFilter = (value: string) => {
    this.dataSource.filter = value.trim().toLocaleLowerCase();
  };
  public doSortAndPaginate(): void {
    this.dataSource.sort = this.sort;
    if (this.hasPaginator == true) {
      this.dataSource.paginator = this.paginator;
    }
    //
  }

  onPageChange(event: PageEvent) {
    this.nextPage.emit(event);
  }
}
