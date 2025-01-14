from sp500 import getCompanies
from intrinsic_value import calculateIntrinsicValue
from flask import Flask, jsonify
from db import connectDB, db, StockPrices, IntrinsicValues
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
connectDB(db)

@app.route('/stock/<company>', methods=['GET'])
async def getStock(company):
    print(company)
    try:
        records = StockPrices.select().where(StockPrices.company == company)
        data = []
        for record in records:
            data.append(model_to_dict(record))
        return jsonify(data)  # Serialize the data to JSON
    except StockPrices.DoesNotExist:
        return "No data found for company: " + company
    
@app.route('/intrinsic/<company>', methods=['GET'])
async def getIntrinsicValue(company):
    print(company)
    try:
        records = IntrinsicValues.select().where(IntrinsicValues.company == company)
        data = []
        for record in records:
            data.append(model_to_dict(record))
        return jsonify(data)  # Serialize the data to JSON
    except IntrinsicValues.DoesNotExist:
        return "No data found for company: " + company

# Return a list of rank values (intrinsic value - most recent stock price), sorted
# {company: string, rankValue: double}
# 
@app.route('/rankingList', methods=['GET'])
async def getRankingList():
    try:
        intrinsicValues = IntrinsicValues.select().order_by(IntrinsicValues.intrinsicValue.desc())
        
        ranking_list = []

        for record in intrinsicValues:
            company = record.company
            mostRecentPriceQuery = StockPrices.select().where(StockPrices.company == str(company)).order_by(StockPrices.date.desc()).limit(1)
            
            # Ensure there's a most recent price record
            if mostRecentPriceQuery.exists():
                mostRecentPrice = mostRecentPriceQuery.get().price  # Assuming your StockPrices model has a 'price' field
                rankValue = record.intrinsicValue - mostRecentPrice
                ranking_list.append({"company": company, "rankValue": rankValue, "stockPrice": mostRecentPrice, "intrinsicValue": record.intrinsicValue})
            else:
                print(f"No stock price found for {company}")

        ranking_list = sorted(ranking_list, key=lambda x: x['rankValue'], reverse=True)  # Set reverse=True if you want it to be in descending order
        return jsonify(ranking_list)  # Serialize the data to JSON
    except IntrinsicValues.DoesNotExist:
        return jsonify({"error": "No instrinsic values found."})
    except Exception as e:
        print(e)  # Log the exception for debugging
        return jsonify({"error": "Server error."}), 500


@app.route('/list', methods=['GET'])
async def getCompanyList():
    try:
        records = IntrinsicValues.select()
        data = []
        for record in records:
            data.append(record.company)
        return data # Serialize the data to JSON
    except IntrinsicValues.DoesNotExist:
        return "No companies found."

if __name__ == '__main__':
    app.run()

db.close()

# companies = getCompanies()
# companies.remove('MNST')
# companies.remove('MPWR')
# companies.remove('ISRG')
# # some companies have different column names and giving us problems...
# # ALL, AXP

# # 33 AWK is -206.11
# # 43 AAPL is 104.38
# count = 1
# for company in companies:
#     intrinsicValue = calculateIntrinsicValue(company)
    
#     print(count,company, ': ', intrinsicValue)
#     newRow = IntrinsicValues.create(company=company, intrinsicValue=intrinsicValue)
#     newRow.save()
#     count += 1

# # Used to load the database with the stock prices over the last 5 years:
# #print(loadStockPriceData(getCompanies()))
