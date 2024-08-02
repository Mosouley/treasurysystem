import { MaterialModule } from './../../../material/material.module';
import { CommonModule } from '@angular/common';
import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { DataModel } from '../../../model/data.model';
import { DataService } from '../../../shared/services/data.service';

@Component({
  selector: 'app-upload-template',
  standalone: true,
  imports: [CommonModule, MaterialModule],
  templateUrl: './upload-template.component.html',
  styleUrl: './upload-template.component.css'
})
export class UploadTemplateComponent  implements OnInit {

  public records: any[] = [];
  @ViewChild('csvReader') csvReader: any;

  // @ViewChild('fileUploadInput')
  // fileUploadInput: any;

  @Input()
  dataModelList!: DataModel[];
  @Input()
  initItem: any;
  importError = false;
  lstColumnNames: string[] = [];
  @Input()
  service!: DataService;

  constructor(

  ) { }

  ngOnInit() {
    this.importError = true;
  }

  uploadListener($event: any): void {

    const text = [];
    const files = $event.srcElement.files;

    this.dataModelList.forEach(col => {
      console.log(col);

      if (col.readonly = true) {
        this.lstColumnNames.push(col.columnName);
      }

    });
    if (this.isValidCSVFile(files[0])) {
      console.log(this.initItem);

      const input = $event.target;
      const reader = new FileReader();
      reader.readAsText(input.files[0]);

      reader.onload = () => {
        const csvData = reader.result;
        const csvRecordsArray = (csvData as string).split(/\r\n|\n/);
        const headersRow = this.getHeaderArray(csvRecordsArray);
        this.records = this.getDataRecordsArrayFromCSVFile(csvRecordsArray, this.dataModelList);
      };

    } else {
      alert('Please import valid .csv file.');
      this.fileReset();
    }
  }

  getDataRecordsArrayFromCSVFile(csvRecordsArray: any, model: DataModel []) {
    const csvArr = [];

    for (let i = 1; i < csvRecordsArray.length; i++) {
      const currentRecord = (<string>csvRecordsArray[i]).split(';');

      if (currentRecord.length === model.length) { // permet de verifier le file importe

          const csvRecordC = new Object();
          model.forEach( (mdel, ind) => {
            switch (mdel.dataType ) {
              case 'string':
                // la propriete est de type string
                // csvRecordC[mdel.columnName] = String(currentRecord[ind]);
                // break;
                // case 'number':
                // // la propriete est de type NUMBER
                // csvRecordC[mdel.columnName] = Number(currentRecord[ind]);
                // break;
                // case 'date':
                // // la propriete est de type NUMBER
                // csvRecordC[mdel.columnName] = new Date(currentRecord[ind]);
                break;
              default:
              this.importError = true;
                break;
            }
          });
          console.log(csvRecordC);

          csvArr.push(csvRecordC);


        this.importError = false;
      } else {
        this.importError = true;
      }
    }
    if (this.importError) {
      alert('Please your data should have same number of columns.');
        this.fileReset();
    }
    return csvArr;
  }

  isValidCSVFile(file: any) {
    return file.name.endsWith('.csv');
  }

  getHeaderArray(csvRecordsArr: any) {
    const headers = (<string>csvRecordsArr[0]).split(';');
    const headerArray = [];
    for (let j = 0; j < headers.length; j++) {
      headerArray.push(headers[j]);
    }

    return headerArray;
  }

  fileReset() {
    this.csvReader.nativeElement.value = '';
    this.records = [];
  }

  uploadData() {
    // uploading the data received
    // this.service.addAll(this.records).subscribe(res => {

    // } );
}
}
