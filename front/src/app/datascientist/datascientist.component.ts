import { Component, OnInit, Input, Output } from '@angular/core';
import { FormControl } from '@angular/forms';

import { DataScientistService } from '../services/datascientist.service';
import {
  IEnums,
  IDataScientistFilter,
  IDataScientistStats,
} from '../interfaces';
import { Options } from 'ng5-slider';

@Component({
  selector: 'app-datascientist',
  templateUrl: './datascientist.component.html',
  styleUrls: ['./datascientist.component.scss'],
})
export class DatascientistComponent implements OnInit {
  @Input()
  title: string;

  mode: string;

  stats: any;
  enums: any;
  filter: IDataScientistFilter;
  thumbLabel = true;
  selectedAmount = 2;
  selectedDistance = 3;

  selectedZoneDep = [];
  selectedZoneArr = [];
  selectedVendorId = [];
  selectedPaymentType = [];
  selectedRateCodeID = [];

  panelOpenState = false;
  zoneDEP = new FormControl();
  zoneARR = new FormControl();
  vendorID = new FormControl();
  paymentType = new FormControl();
  rateCodeID = new FormControl();

  optionsPrix: Options = {
    floor: -100,
    ceil: 999,
  };
  valuePrix: number = this.optionsPrix.floor;
  highValuePrix: number = this.optionsPrix.ceil;

  optionsDist: Options = {
    floor: -100,
    ceil: 999,
  };

  valueDist: number = this.optionsDist.floor;
  highValueDist: number = this.optionsDist.ceil;

  optionsFare: Options = {
    floor: -100,
    ceil: 999,
  };

  valueFare: number = this.optionsFare.floor;
  highValueFare: number = this.optionsFare.ceil;

  optionsExtra: Options = {
    floor: -100,
    ceil: 999,
  };

  valueExtra: number = this.optionsExtra.floor;
  highValueExtra: number = this.optionsExtra.ceil;

  optionsImprov: Options = {
    floor: -100,
    ceil: 999,
  };

  valueImprov: number = this.optionsImprov.floor;
  highValueImprov: number = this.optionsImprov.ceil;

  optionsMta: Options = {
    floor: -100,
    ceil: 999,
  };

  valueMta: number = this.optionsMta.floor;
  highValueMta: number = this.optionsMta.ceil;

  optionsPass: Options = {
    floor: -100,
    ceil: 999,
  };

  valuePass: number = this.optionsPass.floor;
  highValuePass: number = this.optionsPass.ceil;

  optionsTip: Options = {
    floor: -100,
    ceil: 999,
  };

  valueTip: number = this.optionsTip.floor;
  highValueTip: number = this.optionsTip.ceil;

  optionsTolls: Options = {
    floor: -100,
    ceil: 999,
  };

  valueTolls: number = this.optionsTolls.floor;
  highValueTolls: number = this.optionsTolls.ceil;

  showSpinner = false;

  constructor(private dataScientistService: DataScientistService) {}

  ngOnInit() {
    this.title = 'Data Scientist';
    this.mode = 'datascientist';
    this.enums = this.dataScientistService.getEnumsSynchronous();
    this.InitDataScientist(this.enums);
  }

  InitDataScientist(enn: IEnums) {
    this.showSpinner = true;
    this.zoneDEP.setValue(enn.zones);
    this.zoneARR.setValue(enn.zones);
    this.vendorID.setValue(['1', '2']);

    this.paymentType.setValue(['1', '2', '3', '4', '5', '6']);
    this.rateCodeID.setValue(['1', '2', '3', '4', '5', '6']);

    let basicFilter = {
      total_amount_min: this.optionsPrix.floor,
      total_amount_max: this.optionsPrix.ceil,

      trip_distance_min: this.optionsDist.floor,
      trip_distance_max: this.optionsDist.ceil,

      fare_amount_min: this.optionsFare.floor,
      fare_amount_max: this.optionsFare.ceil,

      extra_min: this.optionsExtra.floor,
      extra_max: this.optionsExtra.ceil,

      improvement_surcharge_min: this.optionsImprov.floor,
      improvement_surcharge_max: this.optionsImprov.ceil,

      mta_tax_min: this.optionsMta.floor,
      mta_tax_max: this.optionsMta.ceil,

      passenger_count_min: this.optionsPass.floor,
      passenger_count_max: this.optionsPass.ceil,

      tip_amount_min: this.optionsTip.floor,
      tip_amount_max: this.optionsTip.ceil,

      tolls_amount_min: this.optionsTolls.floor,
      tolls_amount_max: this.optionsTolls.ceil,

      ratecodeid: this.rateCodeID.value,
      payment_type: this.paymentType.value,

      vendorid: this.vendorID.value,
      zone_depart: this.zoneDEP.value,
      zone_arrivee: this.zoneARR.value,
    } as IDataScientistFilter;

    this.dataScientistService
      .getStatsdataScientist(basicFilter)
      .subscribe((data: IDataScientistStats) => {
        this.stats = data;
        this.showSpinner = false;
      });

    console.log('FILTRES BASIC A ENVOYER :', basicFilter);
  }

  selectAll_RateCodeId(ev) {
    if (ev._selected) {
      this.rateCodeID.setValue(this.enums.rate_code);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.rateCodeID.setValue([]);
    }
  }

  selectAll_PaymentType(ev) {
    if (ev._selected) {
      this.paymentType.setValue(this.enums.payment_type);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.paymentType.setValue([]);
    }
  }

  selectAll_zonesDepart(ev) {
    if (ev._selected) {
      this.zoneDEP.setValue(this.enums.zones);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.zoneDEP.setValue([]);
    }
  }

  selectAll_zonesArrivee(ev) {
    if (ev._selected) {
      this.zoneARR.setValue(this.enums.zones);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.zoneARR.setValue([]);
    }
  }
  selectAll_vendorId(ev) {
    let ven = [];

    if (ev._selected) {
      for (let v of this.enums.vendors) {
        ven.push(v['id'].toString());
      }
      this.vendorID.setValue(ven);
      ev._selected = true;
    }
    if (ev._selected == false) {
      this.vendorID.setValue([]);
    }
  }

  postFilter() {
    console.log('Post request function');
    this.showSpinner = true;

    let filters = {
      total_amount_min: parseFloat(this.valuePrix.toString()),
      total_amount_max: parseFloat(this.highValuePrix.toString()),

      trip_distance_min: parseFloat(this.valueDist.toString()),
      trip_distance_max: parseFloat(this.highValueDist.toString()),

      extra_min: parseFloat(this.valuePrix.toString()),
      extra_max: parseFloat(this.highValueDist.toString()),

      improvement_surcharge_min: parseFloat(this.valueDist.toString()),
      improvement_surcharge_max: parseFloat(this.highValueDist.toString()),

      mta_tax_min: parseFloat(this.valueDist.toString()),
      mta_tax_max: parseFloat(this.highValueDist.toString()),

      passenger_count_min: parseFloat(this.valueDist.toString()),
      passenger_count_max: parseFloat(this.highValueDist.toString()),

      tip_amount_min: parseFloat(this.valueDist.toString()),
      tip_amount_max: parseFloat(this.highValueDist.toString()),

      tolls_amount_min: parseFloat(this.valueDist.toString()),
      tolls_amount_max: parseFloat(this.highValueDist.toString()),

      ratecodeid: this.rateCodeID.value,
      payment_type: this.paymentType.value,

      vendorid: this.vendorID.value,
      zone_depart: this.zoneDEP.value,
      zone_arrivee: this.zoneARR.value,
    } as IDataScientistFilter;

    console.log('FILTRES A ENVOYER :', filters);

    this.dataScientistService
      .getStatsdataScientist(filters)
      .subscribe((data: any) => {
        this.stats = data;
        this.showSpinner = false;
      });
  }
}
