export interface MenuNode {
    name: string;
    url?: string;
    icon?: string;
    action?: boolean;
    expandable?: boolean;
    level?: number;
    children?: MenuNode[];
  }
