import { MaterialModule } from './../../../material/material.module';
import { SampleComponent } from './../sample/sample.component';
import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { DataModel } from '../../../model/data.model';
import { DataService } from '../../../shared/services/data.service';
import { UploadTemplateComponent } from '../upload-template/upload-template.component';

@Component({
  selector: 'app-generic',
  standalone: true,
  imports: [CommonModule,
     ReactiveFormsModule,
     MaterialModule,
    SampleComponent,
    UploadTemplateComponent
     ],
  templateUrl: './generic.component.html',
  styleUrl: './generic.component.css'
})
export class GenericComponent {
  crudType = 'sample';

  @Input()
  data: any;

  @Input()
  dataToLoad: any;

  @Input()
  arrayData: any;

  @Input()
  service!: DataService;

  @Input()
  title!: string;

  @Input()
  initItem: any;

  @Input()
  dataModelList!: DataModel[];
  @Input()
  arrayModelList!: DataModel[];
  @Input()
  enumElements = [];
  @Input()
  enumType:any;
  @Input()
  initForm!: FormGroup;

  crudForm!: FormGroup;

  operation = 'add';

  selectedItem: any;

  constructor(private fb: FormBuilder) {
  }

}
