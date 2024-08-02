import { HttpClient } from '@angular/common/http';
import { Component, OnInit, Output } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';



type AOA = any[][];

@Component({
    selector: 'app-import-file',
    templateUrl: './import-file.component.html',
    styles: [],
    standalone: true,
})
export class ImportFileComponent {
  title = 'Bulk Import: Rates';
  disabled = true;
  // @Output() reportingData: any[] = [];
  data!: AOA;
  file: any;
  target!: DataTransfer;
  constructor(
    public dialogRef: MatDialogRef<ImportFileComponent>  ) {}

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
    //     this.data = <AOA>XLSX.utils.sheet_to_json(ws, { header: 1, range: 1  });
    //     this.disabled = false

    //   };
    //  console.log(target.files[0]); //done l'objet File
    //   reader.readAsBinaryString(target.files[0]);
    // } catch (error) {
    //   console.error('Error importing file:', error);
    //   // Handle the error here...
    // }
  }

  project_data() {
    // this.daily.addMany(this.data.slice(1)).subscribe((resp) => {
    // });
    // console.log(this.data);

    this.dialogRef.close(this.data);
  }
}
