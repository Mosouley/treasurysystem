import { PositionUpdateService } from './../../../../shared/services/position-update.service';
import { CommonModule, DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MaterialModule } from '../../../../material/material.module';

@Component({
  selector: 'app-position-update',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule,MaterialModule,
    FormsModule],
  templateUrl: './position-update.component.html',
  styleUrl: './position-update.component.css',
  providers:[DatePipe]
})
export class PositionUpdateComponent implements OnInit{
  positionForm!:FormGroup
  param = []

  constructor(private fb: FormBuilder, 
    private positionService: PositionUpdateService,
    private datePipe: DatePipe){

  }

  ngOnInit(): void {
    this.positionForm = this.fb.group({
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
  })
}

updatePosition(){
  if (this.positionForm.valid) {
    const start_date = this.datePipe.transform(this.positionForm.value.start_date, 'yyyy-MM-dd');
      const end_date = this.datePipe.transform(this.positionForm.value.end_date, 'yyyy-MM-dd');
    
    this.positionService.add({start_date, end_date}).subscribe({
    next: (data)=> {
      console.log(data)

    },
    error: (e) => console.log(e)
    
    
    })
  }
 
}
}
