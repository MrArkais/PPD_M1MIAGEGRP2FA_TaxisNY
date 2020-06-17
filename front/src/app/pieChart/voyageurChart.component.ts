import {
  Component,
  OnInit,
  Input,
  OnChanges,
  SimpleChanges,
  ɵConsole,
} from '@angular/core';

import * as CanvasJS from './canvasjs.min.js';
import { IPieDatas, IPlotDatas } from '../interfaces';

@Component({
  selector: 'app-voyageurChart',
  templateUrl: './voyageurChart.component.html',
  styleUrls: ['./voyageurChart.component.scss'],
})
export class VoyageurChartComponent implements OnInit, OnChanges {
  @Input() statschild: any;



  datasD: IPieDatas[] = [];
  datasA: IPieDatas[] = [];
  datasPayment: IPlotDatas[] = [];

  ngOnChanges(changes: SimpleChanges) {
    if (changes['statschild']) {
      this.buildChart();
    }
  }

  ngOnInit() {
    this.buildChart();
  }


  buildChart() {
    this.datasD = [];
    this.datasA = [];
    this.datasPayment = [];


    let zonesD = this.statschild.zone_depart_distinct;
    let zonesA = this.statschild.zone_arrivee_distinct;
    let paymentType = this.statschild.paiement_type_distinct;


    for (let z of zonesD) {
      let dep = { y: z.count, name: z.zone_depart } as IPieDatas;
      this.datasD.push(dep);
    }

    for (let z of zonesA) {
      let arr = { y: z.count, name: z.zone_arrivee } as IPieDatas;
      this.datasA.push(arr);
    }

    for (let z of paymentType) {


      let pay = { y: z.count, name: z.payment_type } as IPieDatas;

      this.datasPayment.push(pay);

    }

    let chart = new CanvasJS.Chart('chartContainer', {
      theme: 'light2',
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: 'Répartition de zones de départ',
      },
      data: [
        {
          type: 'pie',
          showInLegend: true,
          toolTipContent: '<b>{name}</b>: {y} (#percent%)',
          indexLabel: '{name} - #percent%',
          dataPoints: this.datasD,
        },
      ],
    });

    let chart2 = new CanvasJS.Chart('chartContainer2', {
      theme: 'light2',
      animationEnabled: true,
      exportEnabled: true,
      title: {
        text: "Répartition de zones d'arrivée",
      },
      data: [
        {
          type: 'pie',
          showInLegend: true,
          toolTipContent: '<b>{name}</b>: {y} (#percent%)',
          indexLabel: '{name} - #percent%',
          dataPoints: this.datasA,
        },
      ],
    });


    chart.render();
    chart2.render();

  }
}
