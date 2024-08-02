import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-settings-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './settings-panel.component.html',
  styleUrls: ['./settings-panel.component.css']
})
export class SettingsPanelComponent  {

  @Input() isSettingsPanelOpen = false;
  @Output () toggleSettingsPanel: EventEmitter<boolean> = new EventEmitter<boolean>();


}
