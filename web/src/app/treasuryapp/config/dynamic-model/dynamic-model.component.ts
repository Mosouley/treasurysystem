import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { API_URLS } from './../../../shared/config/app.url.config';
import { Component, OnInit } from '@angular/core';
import { GenericService } from '../../../shared/services/generic.service';
import { GenericComponent } from '../generic/generic.component';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-dynamic-model',
  standalone: true,
  imports: [GenericComponent, CommonModule, ReactiveFormsModule],
  templateUrl: './dynamic-model.component.html',
  styleUrl: './dynamic-model.component.css'
})
export class DynamicModelComponent implements OnInit{
  formElement!: any[];
  apiUrl!: string;
  models: any[] = []
  form!: FormGroup;
  constructor(public genericDataService: GenericService<any>,
    private fb: FormBuilder
  
  ) {}
  ngOnInit(): void {
      this.genericDataService.getAll(API_URLS.MODEL_METADATA_ALL).subscribe( (data: any) => {
        this.models= data   
        
      })
    
      
  }
  selectModel(model: any) {

    
    const selectedModelName = (model.target as HTMLSelectElement).value;
    const selectedModel = this.models.find(model => model.model === selectedModelName);

    
    if (selectedModel) {
      this.formElement = selectedModel.fields;
      this.buildForm()
    }
  }

  buildForm(): void {

    let formControls: any = {};
    if (this.formElement) {
      this.formElement.forEach((field:any) => {
        formControls[field.name] = ['', Validators.required];
      });
      this.form = this.fb.group(formControls);
      
    } else {
      console.log('No form');
      
    }
    
  }
}
