

export const childRoutes =
[
  {
    name: 'Dashboard',
    url: 'dashboard',
    icon: 'speed',
    action: false,
    expandable: false
  },

  {
    name: 'Assets & Liab',
    url: 'profile',
    icon: 'category',
    action: false,
    expandable: true,
    children: [
      {
        name: 'Liquidity',
        url: 'tabsandcards',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'Maturity Profile',
        url: 'analytics',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'Portfolio ',
        url: 'analytics',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'Exposure',
        url: 'outlook',
        icon: 'fingerprint',
        action: false
      },
    ]
  },
  {
    name: 'Sales',
    url: '',
    icon: 'qr_code',
    action: false,
    expandable: true,
    children: [
      {
        name: 'TradeFlow ',
        url: 'tradesflow',
        icon: 'fingerprint',
        action: false
      },

      {
        name: 'Wallet Sizing',
        url: 'walletsizing',
        icon: 'fingerprint',
        action: false
      },
      {
        name: 'FX Blotter',
        url: 'fxblotter',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'FX Flows',
        url: 'fxflows',
        icon: 'contact_page',
        action: false
      },
    ]
  },

  {
    name: 'Trading',
    url: 'dash-ui',
    icon: 'list',
    action: false,
     expandable: true,
    children: [
      {
        name: 'Trading Blotter',
        url: 'profile',
        icon: 'contact_page',
        action: false
      },

    ]
  },

  {
    name: 'Reporting',
    url: 'reporting',
    icon: 'admin_panel_settings',
    action: false,
    expandable: true,
    children: [
      {
        name: 'Periodic Sales',
        url: 'sales-per-period',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'Reporting 2',
        url: 'app1',
        icon: 'fingerprint',
        action: false
      },
    ]
  },

  {
    name: 'Configuration',
    url: 'main',
    icon: 'admin_panel_settings',
    action: false,
    expandable: true,
    children: [
      {
        name: 'Settings',
        url: 'settings',
        icon: 'contact_page',
        action: false
      },
      {
        name: 'Position Update',
        url: 'position-update',
        icon: 'fingerprint',
        action: false
      },
    ]
  },


];
