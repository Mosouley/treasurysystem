
// import { MatInputCommifiedDirective } from './../../shared/custom/mat-input-commified.directive';
import { Currency } from './../../model/currency';
import { Component, Inject, OnInit } from '@angular/core';

import { FormBuilder, FormGroup, Validators, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogContent, MatDialogActions, MatDialogClose } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';

import { CurrencyPipe, DecimalPipe, NgFor, NgIf } from '@angular/common';
// import { Pnl_Calculation } from 'src/app/shared/custom/trade-functions';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { Customer } from '../../model/customer';
import { Product } from '../../model/product';
import { DailyRateService } from '../../shared/services/dailyrates.service';


interface Option {
  value: string;
  viewValue: string;
}

@Component({
    selector: 'app-trade',
    templateUrl: './trade.component.html',
    styleUrls: ['./trade.component.css'],
    standalone: true,
    imports: [
        MatDialogContent,
        FormsModule,
        ReactiveFormsModule,
        MatFormFieldModule,
        MatSelectModule,
        NgFor,
        MatOptionModule,
        MatInputModule,
        MatDatepickerModule,
        NgIf,
        MatDialogActions,
        MatButtonModule,
        MatDialogClose,
    ],
})
export class TradeComponent implements OnInit {
  public tradeForm!: FormGroup;
  public products: Product[] = [];
  public filteredProduits: Product[] = [];
  public customers: Customer[] = [];
  public currencies: Currency[] = [];
  public totalSum = 0;
  public tradeFormValueChanges$!: Observable<any>;
  public myFormCategoryChanges$!: Observable<any>;
  public myFormProduitChanges$!: Observable<any>;
  public selectedRowData: any;
  color = 'blue';
  disabled = false;
  focused = true;
  private ccy1_rate = 1;
  private ccy2_rate = 1;
  private syst_rate = 1;
   amount1Formatted = 0;
  // private selectedProduit!: Product;
  buySells: any[] = [
    { value: 'buy', viewValue: 'Buy' },
    { value: 'sell', viewValue: 'Sell' },
  ];
  ccyPair: { value: string; viewValue: string }[] = [];

  private currentDate = new Date().toISOString().substring(0, 16);
  constructor(
    private fb: FormBuilder,
    private aRoute: ActivatedRoute,
    @Inject(MAT_DIALOG_DATA) public receiveData: any,
    private dialogRef: MatDialogRef<TradeComponent>,
    private rate_service: DailyRateService,
    // private decimalPipe: DecimalPipe, private matDir: MatInputCommifiedDirective,

    private decimalPipe: DecimalPipe,
    private currencyPipe: CurrencyPipe
  ) {}

  ngOnInit() {
    this.currencies = this.receiveData['currencies']; //this.receiveData.products;
    this.products = this.receiveData['products']; //this.receiveData.products;
    this.customers = this.receiveData['customers']; //this.receiveData.products;
    // this.selectedRowData = this.receiveData.selectedRow;
    this.initData();

    // Subscribe to value changes for both currency inputs
    this.tradeForm.controls['ccy1'].valueChanges.subscribe(
      this.createCcyPairOptions
    );
    this.tradeForm.controls['ccy2'].valueChanges.subscribe(
      this.createCcyPairOptions
    );


    this.tradeForm.valueChanges.subscribe((form) => {
      if (form.amount1 !== null && form.amount1 !== undefined) {
        // Remove non-numeric characters (including commas and spaces)
        let numericValue = form.amount1.toString().replace(/[^0-9.]/g, '');

        // Check if the input is not empty and is a valid number
        if (numericValue !== '' && !isNaN(numericValue)) {
          // Parse the cleaned numeric value
          const parsedValue = parseFloat(numericValue);

          // Format the parsed value and store it
          // this.amount1Formatted = this.currencyPipe.transform(parsedValue, '', '', '1.0-2');

          // Update the form control with the formatted value
          this.tradeForm.patchValue({ amount1: this.currencyPipe.transform(parsedValue, '', '', '1.0-2')}, { emitEvent: false });
        }
      }
    });
      // this.tradeForm.valueChanges.subscribe( form => {
      //   if(form.amount1 !== null && form.amount1 !== undefined){

      //     let numericValue = form.amount1.toString().replace(/,/g, ''); // Remove commas
      //     numericValue = numericValue.replace(/[^0-9.]/g, ''); // Allow numeric digits and decimal point
      //     numericValue = numericValue.replace(/^0+/,''); // Remove leading zeros
      //     numericValue = parseFloat(numericValue)
      //    // Check if the input is a valid number
      //    if (!isNaN(numericValue) && numericValue !== '' ) {
      //     this.amount1Formatted = parseFloat(this.currencyPipe.transform(numericValue, '', '', '1.0-2'));

      //     this.tradeForm.patchValue({ amount1: this.amount1Formatted }, { emitEvent: false });
      //   }
      //     // this.tradeForm.patchValue({
      //     //   amount1: this.currencyPipe.transform(form.amount1.replace(/\D|\./g,'').replace(/^0+/,''), 'USD', 'symbol','1.0-2')
      //     // }, {emitEvent: false});
      //   }
      // });
    // calculate amount2 based on value in amount1
    this.tradeForm.controls['amount1'].valueChanges.subscribe((amount) => {
      this.tradeForm.controls['amount2'].setValue(
        this.amount1Formatted * (this.tradeForm.controls['deal_rate'].value)
      );
    });

    // calculate amount2 based on value in amount1
    this.tradeForm.controls['deal_rate'].valueChanges.subscribe((rate) => {
      this.tradeForm.controls['amount2'].setValue(
        rate * this.tradeForm.controls['amount1'].value
      );
    });
    this.tradeForm.controls['ccy1'].valueChanges.subscribe( x => {
      this.get_Ccy_Rate(this.tradeForm.controls['ccy1'].value).then(rate => {
        this.ccy1_rate = rate
      }).catch(error => {
        console.error('Error:', error);
      });
    });
    this.tradeForm.controls['ccy2'].valueChanges.subscribe( x => {

    this.get_Ccy_Rate(this.tradeForm.controls['ccy2'].value).then(rate => {
      this.ccy2_rate = rate

    }).catch(error => {
      console.error('Error:', error);
    });
    });
    this.tradeForm.controls['ccy_pair'].valueChanges.subscribe( x => {
     this.syst_rate = this.ccy1_rate / this.ccy2_rate;
     this.tradeForm.controls['system_rate'].setValue(this.syst_rate);
    });

  //   this.tradeForm.valueChanges.subscribe(v => {
  //     if (this.can_calculate_pnl() == true) {
  //       this.calculate_PnL();
  //     }
  // });


  }

  initData() {
    this.createForm();
  }
  // create the form if it does not exist
  createForm() {
    // const numberPatern = '^[0-9.,]+$';
    this.tradeForm = this.fb.group({
      trade_id: [{ value: 'ID- ' + Date.now(), disabled: true }],
      customer: ['', Validators.required],
      product: ['', Validators.required],
      value_date: ['', Validators.required],
      deal_date: ['', Validators.required],
      booking_date: [{ value: this.currentDate, disabled: true }],
      ccy1: ['', Validators.required],
      ccy2: ['', Validators.required],
      ccy_pair: ['', Validators.required],
      buy_sell: ['', Validators.required],
      amount1: ['', [Validators.required, Validators.pattern(/^\d+(\.\d{1,2})?$/)]],
      amount2: [{ value: '', disabled: true }],
      deal_rate: ['', Validators.required],
      fees_rate: [''],
      tx_comments: [''],
      system_rate: [{ value: '', disabled: true }],
      cover_rate: [{ value: '', disabled: true }],
      gross_pnl: [{ value: '', disabled: true }],
      net_pnl: [{ value: '', disabled: true }, Validators.required],
    });
    // this.tradeForm.get('amount1')?.patchValue(this.decimalPipe.transform(0, '1.0-2'));
  }

  // formatInput(event: any) {
  //   const value = event.target.value.replace(/,/g, '').replace(/ /g, ''); // Remove commas and spaces
  //   if (!isNaN(value)) {
  //     this.tradeForm.get('amount1')!.setValue(parseFloat(value));
  //   }
  //   this.amount1Formatted = this.currencyPipe.transform(value, '', '', '1.0-2');
  // }

  // Define a function that creates the currency pair options
  createCcyPairOptions = () => {
    const ccy1 = this.tradeForm.controls['ccy1'].value;
    const ccy2 = this.tradeForm.controls['ccy2'].value;
    this.ccyPair = [
      { value: 'ccy1/ccy2', viewValue: `${ccy1}/${ccy2}` },
      { value: 'ccy2/ccy1', viewValue: `${ccy2}/${ccy1}` },
    ];
  };
  // Function that generates a trade id from a the date
  /* Date */
  date(e: any) {
    var convertDate = new Date(e.target.value).toISOString().substring(0, 10);
    this.tradeForm.get('value_date')!.setValue(convertDate, {
      onlyself: true,
    });
  }
  onCancel(): void {
    this.dialogRef.close();
  }

  onSubmit(): void {

    // console.warn (this.tradeForm.value)
    // Handle form submission here
    this.dialogRef.close(this.tradeForm.value)
  }

  /*
  Function to calculate the PnL on the trade
  */
  // calculate_PnL(){

  //   let ccy1_amount = this.tradeForm.controls['amount1'].value;
  //   let deal_rate = this.tradeForm.controls['deal_rate'].value;
  //   // this.tradeForm.controls['ccy2'].setValue(syst_rate)
  //   const pnl = Pnl_Calculation.calculate_pnl(this.ccy2_rate, ccy1_amount, deal_rate, this.syst_rate)


  // }

  get_Ccy_Rate(ccy: Currency): Promise<number> {
    return new Promise<number>((resolve, reject) => {
      this.rate_service.get(ccy).subscribe(
        (rate:any) => {
          resolve(rate.rateLcy);
        },
        (error:any) => {
          console.error('API call error:', error);
          reject(error);
        }
      );
    });
  }


  get_system_rate (ccy1: Currency, ccy2: Currency): number {

    return 1;
  }

  can_calculate_pnl(): boolean {
    if (
      this.tradeForm.controls['ccy2'].valid &&
      this.tradeForm.controls['amount1'].valid &&
      this.tradeForm.controls['deal_rate'].valid
    ) {
      return true
    } else {
      return false;
    }

  }

}


