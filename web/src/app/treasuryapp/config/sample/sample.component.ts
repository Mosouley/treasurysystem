import { MaterialModule } from './../../../material/material.module';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { DataModel } from '../../../model/data.model';
import { DataService } from '../../../shared/services/data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sample',
  standalone: true,
  imports: [CommonModule, MaterialModule, FormsModule, ReactiveFormsModule],
  templateUrl: './sample.component.html',
  styleUrl: './sample.component.css'
})
export class SampleComponent {

  @Input()
  data: any;

  @Input()
  arrayData!:any;

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
  initForm!: FormGroup;

  crudForm!: FormGroup;
 panelOpenState = false;
  operation = 'add';

  myformValueChange$: any;
  selectedItem: any;

  @Input()
  enumElements:any = [] ;
  @Input()
  enumType: any;

  @Output ()
  selectedItemChange: EventEmitter<boolean> = new EventEmitter<boolean>();



  constructor(private fb: FormBuilder,

  ) {
    this.createForm();

  }

  ngOnInit() {
    this.initData();
    if (this.enumType != null) {
    this.enumElements = Object.keys(this.enumType).filter(f => !isNaN(Number(f)));
    }
    this.myformValueChange$ =  this.crudForm.valueChanges;
    this.myformValueChange$.subscribe( (val: any) => {
      // console.log(val);

    });
    // this.onChange();
  }

  getValues($event: any) {
    // console.log(this.selectedItem);
    this.crudForm.patchValue(this.selectedItem);
    // console.log(this.crudForm.value);
    // console.log(this.selectedItem);

  }

  onChange(event: any) {
    this.crudForm.valueChanges.subscribe(val => {
      this.selectedItem = this.crudForm.value;
      this.selectedItemChange.emit(this.selectedItem);
      //  console.log(this.selectedItem);
    });
  }
  createForm() {

    this.initForm ? this.crudForm = this.initForm : this.crudForm = this.fb.group({}) ;
  }

  loadData() {
    // this.service.getAll().subscribe(data => {
    //   this.data = data;
    // });
  }

  add() {
    const p = this.crudForm.value;
    // this.service.create(p).subscribe(res => {
    //   this.loadData();

    // });
    this.initData();
  }

  update() {
      console.log(this.selectedItem);
    // this.service.update(this.selectedItem).subscribe(res => {
    //   this.initData();
    //   this.loadData();
    //   this.toastr.success('Mise a jour effectuee avec succes : Ref ' + this.selectedItem);
    // }, err => this.toastr.error('Attention, mise a jour echouee ')
    // );
  }

  initData() {
    this.selectedItem = this.initItem;
    this.createForm();
  }

  delete() {
    // this.service.delete(this.selectedItem.id).subscribe(res => {
    //   this.selectedItem = this.initItem;
    //   this.toastr.success('Suppression effectuee avec succes : Ref ' + this.selectedItem.id);
    //   this.loadData();
    // });
  }
}
