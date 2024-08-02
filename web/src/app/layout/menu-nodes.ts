export const menuNodes = [
  {
    name: 'Dashboard',
    url: 'dashboard',
    icon: 'bx bx-lock',
    active: false,
    subMenuHeight: '0px',
  },

  {
    name: 'Assets & Liab',
    url: '',
    icon: 'bx bx-category',
    active: false,
    subMenuHeight: '0px',
    subMenu: [
      {
        name: 'Liquidity',
        url: 'tabsandcards',
        icon: 'bx bxs-contact',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Maturity Profile',
        url: 'bx bx-analyse',
        icon: 'bx bxl-microsoft-teams',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Portfolio ',
        url: 'bx bx-analyse',
        icon: 'bx bxl-microsoft-teams',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Exposure',
        url: 'outlook',
        icon: 'bx bxl-microsoft-teams',
        active: false,
        subMenuHeight: '0px',
      },
    ],
  },
  {
    name: 'Sales',
    url: '',
    icon: 'bx bxl-jquery',
    active: false,
    subMenuHeight: '0px',
    subMenu: [
      {
        name: 'TradeFlow ',
        url: 'tradesflow',
        icon: 'bx bx-candles',
        active: false,
        subMenuHeight: '0px',
      },

      {
        name: 'Wallet Sizing',
        url: 'walletsizing',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'FX Blotter',
        url: 'fxblotter',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'FX Flows',
        url: 'bx bx-euro',
        icon: 'contact_page',
        active: false,
        subMenuHeight: '0px',
      },
    ],
  },

  {
    name: 'Trading',
    url: '',
    icon: 'bx bx-qr-scan',
    active: false,
    subMenuHeight: '0px',
    subMenu: [
      {
        name: 'Trading Blotter',
        url: 'profile',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
    ],
  },

  {
    name: 'Reporting',
    url: '',
    icon: 'bx bxs-report',
    active: false,
    subMenuHeight: '0px',
    subMenu: [
      {
        name: 'Periodic Sales',
        url: 'sales-per-period',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Reporting 2',
        url: 'app1',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
    ],
  },

  {
    name: 'Configuration',
    url: '',
    icon: 'bx bx-cog',
    active: false,
    subMenuHeight: '0px',
    subMenu: [
      {
        name: 'Settings',
        url: 'settings',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Model Config.',
        url: 'model-configuration',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      },
      {
        name: 'Config. Entities',
        url: 'entity-configuration',
        icon: 'bx bx-euro',
        active: false,
        subMenuHeight: '0px',
      }
    ],
  },
];
