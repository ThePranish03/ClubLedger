from flask import Flask, request
import algokit_utils
from smart_contracts.artifacts.clubledger.clubledger_client import ClubledgerFactory


app = Flask(__name__)

# Connect to LocalNet
algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment("DEPLOYER")

factory = algorand.client.get_typed_app_factory(
    ClubledgerFactory,
    default_sender=deployer.address
)

# Replace with your App ID
APP_ID = 1011
app_client = factory.get_app_client_by_id(APP_ID)

# Simple in-memory storage
users = []


@app.route("/")
def home():
    return """
    <h2>College Fund System</h2>
    <a href='/admin'>Admin</a><br>
    <a href='/sponsor'>Sponsor</a><br>
    <a href='/club'>Club</a><br>
    <a href='/student'>Student</a><br>
    """


@app.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    if request.method == "POST":
        name = request.form["name"]
        amount = int(request.form["amount"])

        result = app_client.send.sponsor_fund((amount,))
        balance = app_client.state.global_state.total_funds

        users.append({"name": name, "role": "Sponsor"})

        return f"""
        Sponsor: {name}<br>
        Transaction ID: {result.tx_id}<br>
        Updated Balance: {balance}<br>
        <a href='/'>Back</a>
        """

    return """
    <h3>Sponsor Page</h3>
    <form method="post">
        Name: <input name="name"><br>
        Amount: <input name="amount"><br>
        <button type="submit">Fund</button>
    </form>
    """


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        amount = int(request.form["amount"])

        result = app_client.send.transfer_to_club((amount,))
        balance = app_client.state.global_state.total_funds

        return f"""
        Admin transferred {amount}<br>
        Transaction ID: {result.tx_id}<br>
        Updated Balance: {balance}<br>
        <a href='/'>Back</a>
        """

    return """
    <h3>Admin Page</h3>
    <form method="post">
        Transfer Amount: <input name="amount"><br>
        <button type="submit">Transfer to Club</button>
    </form>
    """


@app.route("/club")
def club():
    balance = app_client.state.global_state.total_funds
    return f"""
    <h3>Club Dashboard</h3>
    Current Balance: {balance}<br>
    <a href='/'>Back</a>
    """


@app.route("/student")
def student():
    return """
    <h3>Student Page</h3>
    Event viewing only.<br>
    <a href='/'>Back</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
