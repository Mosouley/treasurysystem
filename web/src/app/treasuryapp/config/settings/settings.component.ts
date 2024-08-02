import { CommonModule } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { NavbarComponent } from '../../../layout/navbar/navbar.component';
import { MaterialModule } from '../../../material/material.module';
import { ApiResponse } from '../../../model/daily_rate';
import { DataModel } from '../../../model/data.model';
import { ReportComponent } from '../../../report/report-template/report.component';
import { DailyRateService } from '../../../shared/services/dailyrates.service';
import { ImportFileComponent } from '../import-file.component';
import { PositionUpdateComponent } from './position-update/position-update.component';
import { CustomerComponent } from "../../../shared/entities/customer/customer.component";


type AOA = any[][];

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule,
    NavbarComponent,
    ReportComponent,
    PositionUpdateComponent,
    CustomerComponent
],
})
export class SettingsComponent implements OnInit {
  dataFetched!: ApiResponse;
  reportingData!: any[];
  newRates: any[] =[];
  // model: DataModel[] = [];
  modelArrayEntity!: DataModel[];
  data!: AOA;
  dataSize=0;

  model = [
    new DataModel('date', 'Date', 'date', false, [], 'date'),
    new DataModel('ccy_code', 'Currency', 'string', false, 'code','uppercase'),
    new DataModel('rateLcy', 'Rate', 'number', false, []),
    new DataModel('last_updated', 'Last. Up', 'date', false, []),
  ];
  constructor(
    @Inject(MatDialog) private dialog: MatDialog,
    private daily: DailyRateService
  ) {}
  ngOnInit(): void {

    this.retrievRates();

  }


  onFileChange(evt: any) {
    /* wire up file reader */

    const target: DataTransfer = <DataTransfer>evt.target;

    if (target.files.length !== 1) throw new Error('Cannot use multiple files');
    const reader: FileReader = new FileReader();

    // try {
    //   reader.onload = (e: any) => {
    //     /* read workbook */
    //     const bstr: string = e.target.result;
    //     const wb: XLSX.WorkBook = XLSX.read(bstr, { type: 'binary' });

    //     /* grab first sheet */
    //     const wsname: string = wb.SheetNames[0];
    //     const ws: XLSX.WorkSheet = wb.Sheets[wsname];

    //     /* save data */
    //     this.data = <AOA>XLSX.utils.sheet_to_json(ws, { header: 1 });
    //     // console.log(this.data);
    //     this.reportingData = this.data
    //    // console.log(this.reportingData);
    //   };
    //  // console.log(target.files[0]); //done l'objet File

    //   reader.readAsBinaryString(target.files[0]);
    // } catch (error) {
    //   console.error('Error importing file:', error);
    //   // Handle the error here...
    // }
  }

  importFile() {
    document.getElementById('fileInput')!.click();
  }
  saveData() {
    // console.info(this.newRates.slice(1))
    this.daily.addMany(this.newRates).subscribe((resp) => {
      this.newRates = []

    });

  }

  retrievRates() {
    this.daily.listAll().subscribe((response: any) => {
      this.dataFetched = response.results
      this.dataSize = response.count
    });

  }
  loadNextPage(event: any) {
    // Perform action to fetch data for the next or previous page using the provided URL
    // Example: Call a service method to fetch data based on the URL
    const pageSize = event.pageSize;
    const currentPage = event.pageIndex;
    const offset = pageSize * currentPage;

    this.daily.fetchData({pageSize, offset}).subscribe(data => {
      this.dataFetched = data.results

    })

  }

  importingFile() {
    const dialogConfig = new MatDialogConfig();
    // dialogConfig.disableClose = false;
    // dialogConfig.autoFocus = true;
    dialogConfig.height = '300px'; // Modify properties directly
    dialogConfig.width = '500px'; // Modify properties directly

    const dialogRef = this.dialog.open(ImportFileComponent, dialogConfig);

    dialogRef.afterClosed().subscribe((result) => {
      this.newRates = result;
      // this.router.navigate(['.'], { relativeTo: this.route });
    });
  }
}
