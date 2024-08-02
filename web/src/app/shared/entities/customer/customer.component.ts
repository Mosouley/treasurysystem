import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { GenericComponent } from '../../../treasuryapp/config/generic/generic.component';
import { DataModel } from '../../../model/data.model';
import { Customer } from '../../../model/customer';
import { CustomerService } from '../../services/customer.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-customer',
  standalone: true,
  imports: [GenericComponent, ReactiveFormsModule],
  templateUrl: './customer.component.html',
  styleUrl: './customer.component.css'
})
export class CustomerComponent implements OnInit {

  customers!: any[];

  customerForm!: FormGroup;

    customer: Customer = new Customer();

  customerModel!: DataModel[];

  constructor(public customerService: CustomerService,
    private fb: FormBuilder, private route: ActivatedRoute) {
}
  ngOnInit() {
    // this.clientService.getAll().subscribe(
    //   response => {
    //     this.clients = response as Client[];
    //   }

    // );
    this.customers = this.route.snapshot.data['customers'];

    this.customerForm = this.fb.group({

      nameClient: ['', Validators.required],
      codeIfuClient: ['', Validators.required],
      phoneClient: ['', Validators.required]

    });

    this.customerModel = [
      new DataModel('id', 'ID', 'number', true, []),
      new DataModel('nameClient', 'Nom Client', 'string', false, []),
      new DataModel('codeIfuClient', 'Code Ifu', 'string', false, []),
      new DataModel('phoneClient', 'Phone', 'string', false, [])


    ];
  }
}
