ClubLedger – Blockchain Based College Club Finance & Event Management System

This starter full stack project has been generated using AlgoKit. See below for default getting started instructions. ClubLedger is a decentralized finance and event management platform built on the Algorand blockchain to ensure transparency, trust, and tamper-proof financial records for college clubs.

It solves real-world problems in college event management such as:
  1.Misuse of funds
  2.Lack of sponsor transparency
  3.Manual ticket accounting
  4.Unclear expense tracking
  5.Trust issues between students and club admins
ClubLedger makes all financial activities verifiable on-chain.

Project Objective
  To build a transparent, decentralized financial ledger system for:
    1.Club account management
    2.Event fund collection
    3.Sponsor tracking
    4.Ticket selling to students
    5.Expense management
    6.Real-time auditability
Using Algorand Smart Contracts (ASC1) and a React frontend.

## Setup

### Initial setup
1. Clone this repository to your local machine.
2. Ensure [Docker](https://www.docker.com/) is installed and operational. Then, install `AlgoKit` following this [guide](https://github.com/algorandfoundation/algokit-cli#install).
3. Run `algokit project bootstrap all` in the project directory. This command sets up your environment by installing necessary dependencies, setting up a Python virtual environment, and preparing your `.env` file.
4. In the case of a smart contract project, execute `algokit generate env-file -a target_network localnet` from the `clubledger-contracts` directory to create a `.env.localnet` file with default configuration for `localnet`.
5. To build your project, execute `algokit project run build`. This compiles your project and prepares it for running.
6. For project-specific instructions, refer to the READMEs of the child projects:
   - Smart Contracts: [clubledger-contracts](projects/clubledger-contracts/README.md)
   - Frontend Application: [clubledger-frontend](projects/clubledger-frontend/README.md)

> This project is structured as a monorepo, refer to the [documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/project/run.md) to learn more about custom command orchestration via `algokit project run`.

### Subsequently

1. If you update to the latest source code and there are new dependencies, you will need to run `algokit project bootstrap all` again.
2. Follow step 3 above.

### Continuous Integration / Continuous Deployment (CI/CD)

This project uses [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions) to define CI/CD workflows, which are located in the [`.github/workflows`](./.github/workflows) folder. You can configure these actions to suit your project's needs, including CI checks, audits, linting, type checking, testing, and deployments to TestNet.

For pushes to `main` branch, after the above checks pass, the following deployment actions are performed:
  - The smart contract(s) are deployed to TestNet using [AlgoNode](https://algonode.io).
  - The frontend application is deployed to a provider of your choice (Vercel). See [frontend README](frontend/README.md) for more information.

> Please note deployment of smart contracts is done via `algokit deploy` command which can be invoked both via CI as seen on this project, or locally. For more information on how to use `algokit deploy` please see [AlgoKit documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/features/deploy.md).

## Tools

This project makes use of Python and React to build Algorand smart contracts and to provide a base project configuration to develop frontends for your Algorand dApps and interactions with smart contracts. The following tools are in use:

- Algorand, AlgoKit, and AlgoKit Utils
- Python dependencies including Poetry, Black, Ruff or Flake8, mypy, pytest, and pip-audit
- React and related dependencies including AlgoKit Utils, Tailwind CSS, daisyUI, use-wallet, npm, jest, playwright, Prettier, ESLint, and Github Actions workflows for build validation

### VS Code

It has also been configured to have a productive dev experience out of the box in [VS Code](https://code.visualstudio.com/), see the [backend .vscode](./backend/.vscode) and [frontend .vscode](./frontend/.vscode) folders for more details.

## Integrating with smart contracts and application clients

Refer to the [clubledger-contracts](projects/clubledger-contracts/README.md) folder for overview of working with smart contracts, [projects/clubledger-frontend](projects/clubledger-frontend/README.md) for overview of the React project and the [projects/clubledger-frontend/contracts](projects/clubledger-frontend/src/contracts/README.md) folder for README on adding new smart contracts from backend as application clients on your frontend. The templates provided in these folders will help you get started.
When you compile and generate smart contract artifacts, your frontend component will automatically generate typescript application clients from smart contract artifacts and move them to `frontend/src/contracts` folder, see [`generate:app-clients` in package.json](projects/clubledger-frontend/package.json). Afterwards, you are free to import and use them in your frontend application.

The frontend starter also provides an example of interactions with your ClubledgerClient in [`AppCalls.tsx`](projects/clubledger-frontend/src/components/AppCalls.tsx) component by default.

###System Architecture

##Frontend (React + Tailwind):
 Student dashboard
 Admin dashboard
 Event creation page
 Ticket buying interface
 Sponsor panel
 Smart Contracts (Python + AlgoKit)

##Club Account Contract:
 Event Contract
 Ticket Sale Logic
 Sponsor Fund Logic
 Expense Approval Logic

##Blockchain Layer (Algorand):
 Stores financial transactions
 Verifies ticket payments
 Maintains immutable ledger


###Functional Modules
1. Club Account Module:
  Create club treasury wallet
  View balance
  Track all transactions on-chain
  Immutable expense log

2. Event Management Module:
Admin can:
  Create event
  Define ticket price
  Set maximum tickets
  Add sponsors
Smart Contract stores:
  Event ID
  Ticket limit
  Total collected funds
  Sponsor details

3. Ticket Selling Module
Process:
  Student connects wallet
  Approves payment
  Atomic transaction executes
  Ticket ASA transferred
  Contract updates ticket count
All transactions recorded on-chain.

4. Sponsor Management Module
Sponsors can:
  Fund event wallet
  Receive on-chain proof
  View fund usage
Ensures:
  Transparent sponsorship
  Tamper-proof contribution records

5. Expense Tracking Module
Admin submits:
  Expense description
   Amount
  Vendor details
Smart contract:
  Deducts from treasury
  Logs transaction
  Makes expense publicly auditable
