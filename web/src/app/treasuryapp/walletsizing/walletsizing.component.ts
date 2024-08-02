import { Component } from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';


interface Element {
  position: number;
  name: string;
  weight: number;
}

const ELEMENT_DATA: Element[] = [
  { position: 1, name: 'Hydrogen', weight: 1.0079 },
  { position: 2, name: 'Helium', weight: 4.0026 },
  { position: 3, name: 'Lithium', weight: 6.941 },
  { position: 4, name: 'Braaaa', weight: 6.941 },
  { position: 5, name: 'toooo', weight: 6.941 },
  { position: 6, name: 'lefft', weight: 6.941 },
  // ...
];
@Component({
    selector: 'app-walletsizing',
    templateUrl: './walletsizing.component.html',
    styleUrls: ['./walletsizing.component.css'],
    standalone: true,
    imports: [MatTableModule, MatSortModule]
})
export class WalletsizingComponent {

  displayedColumns: string[] = ['position', 'name', 'weight'];
  dataSource = new MatTableDataSource(ELEMENT_DATA);

}
