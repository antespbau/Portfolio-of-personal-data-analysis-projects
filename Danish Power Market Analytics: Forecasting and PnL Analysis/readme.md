# Global Bunkering Price Arbitrage Analysis: VLSFO Port Spreads and Route-Based Savings

This project builds an end-to-end data analysis workflow to study VLSFO bunker fuel price differences across major global bunkering ports. The workflow covers data collection, data cleaning, exploratory price analysis, spread calculation, route-based arbitrage modelling and final visualisation.

The objective of the project is not only to compare bunker fuel prices across ports, but to assess whether these price differences can be transformed into practical commercial decisions: bunkering earlier in a cheaper port instead of buying fuel later in a more expensive destination.

---

# FIRST PART OF THE PROJECT

# Project Overview

Bunker fuel is one of the most important operating costs for vessels. After IMO 2020, many vessels without scrubbers shifted towards VLSFO in order to comply with the 0.5% sulphur limit.

However, VLSFO prices are not equal across ports. Differences between ports can create potential arbitrage opportunities, especially when a vessel is sailing through several major bunkering hubs. A cheaper port does not automatically represent a real opportunity, because the vessel also needs to consider route feasibility, fuel consumption, tank capacity, port costs and timing.

This project develops a simplified analytical framework to identify where price differences appear, how large those differences are, and whether they remain attractive after applying basic operational assumptions.

---

# 1. VLSFO Price Collection and Cleaning

The first stage of the project focuses on collecting recent VLSFO bunker price data from public Ship & Bunker port pages.

The selected ports are:

* Rotterdam
* Gibraltar
* Houston
* Singapore
* Fujairah

These ports were selected because they represent important global bunkering hubs across Europe, the Mediterranean, the Middle East, Asia and the Americas.

The raw scraped data was cleaned and transformed into a structured VLSFO historical price dataset. Only VLSFO observations were kept for the final analysis, because the purpose of the first version of the project is to focus on one standard marine fuel product.

---

# 2. VLSFO Price Evolution by Port

## Exploratory visualisation

<p align="center">
  <img src="outputs/charts/vlsfo_price_evolution_by_port.png" width="900"/>
</p>

The price evolution chart shows clear differences between the selected bunkering ports. Rotterdam and Gibraltar remain consistently among the cheapest ports during the analysed period, while Fujairah shows significantly higher VLSFO prices.

Fujairah also presents stronger movements over time, especially from the beginning of June onwards. This is relevant from a commercial point of view because a higher price level combined with stronger volatility can create larger spreads, but also greater uncertainty.

---

# 3. Average VLSFO Price Comparison

## Average price by port

<p align="center">
  <img src="outputs/charts/average_vlsfo_price_by_port.png" width="900"/>
</p>

The average price comparison highlights the main structure of the market sample. Rotterdam is the cheapest port on average, followed by Gibraltar. Houston and Singapore remain in the middle of the price range, while Fujairah is clearly the most expensive port in the dataset.

This result suggests that, for vessels sailing from Europe towards the Middle East, buying VLSFO earlier in Rotterdam or Gibraltar could be more attractive than waiting to bunker in Fujairah.

---

# 4. Daily Price Spread Analysis

## Fujairah vs Rotterdam spread

<p align="center">
  <img src="outputs/charts/daily_spread_fujairah_vs_rotterdam.png" width="900"/>
</p>

The spread between Fujairah and Rotterdam is one of the most important indicators in the project. It measures how much more expensive Fujairah is compared with Rotterdam on each day.

A positive spread means that Rotterdam is cheaper than Fujairah. The larger the spread, the stronger the potential gross saving from buying fuel in Rotterdam instead of Fujairah.

During the analysed period, the Fujairah-Rotterdam spread remains positive every day. The spread also increases sharply in early June, showing how quickly bunker price differences can become commercially significant.

---

# SECOND PART OF THE PROJECT — ROUTE ARBITRAGE

# 5. Route-Based Arbitrage Model

## Motivation

A simple price comparison is not enough to support a commercial bunkering decision. A vessel cannot always choose the cheapest port in the world. The port must be located on or near the vessel’s route, and the vessel must have enough tank capacity to carry the fuel required for the next legs of the voyage.

For this reason, the project extends the analysis into a route-based arbitrage model.

The first version of the model focuses on a Europe to Fujairah route and compares two alternative bunkering decisions:

* bunker earlier in Rotterdam
* bunker earlier in Gibraltar
* compare both alternatives against buying in Fujairah

The model estimates the gross saving from the price spread and then subtracts simplified extra costs such as port call cost, delay cost and a basic risk buffer.

---

# 6. Net Saving Analysis

## Net saving by alternative bunker port

<p align="center">
  <img src="outputs/charts/net_saving_by_date_and_alternative_port.png" width="900"/>
</p>

The net saving chart shows the estimated daily savings from bunkering earlier in Rotterdam or Gibraltar instead of buying VLSFO in Fujairah.

Both alternatives remain profitable in the simplified model. Rotterdam generally produces the highest estimated saving because it has the lowest average VLSFO price in the dataset. Gibraltar also remains attractive, although its savings are slightly lower because its prices are higher than Rotterdam and the model includes additional timing assumptions.

The results suggest that route-based bunker procurement can create meaningful savings when price differences between ports are large enough to compensate for operational costs and timing risk.

---

# 7. Vessel Fuel Requirement Calculation

The project also includes a basic vessel fuel requirement calculation by route leg and vessel type.

The model uses simplified vessel profiles with:

* vessel speed
* daily fuel consumption
* tank capacity
* daily vessel cost
* safety reserve percentage

For each route leg, the model estimates:

* voyage days
* fuel required without reserve
* fuel required with safety reserve

This step is important because bunker arbitrage is not only about price. A vessel must physically be able to carry enough fuel to reach the next port or destination safely.

---

# 8. Key Results

| Area                     | Main Result               |
| ------------------------ | ------------------------- |
| Cheapest port            | Rotterdam                 |
| Second cheapest port     | Gibraltar                 |
| Most expensive port      | Fujairah                  |
| Highest volatility       | Fujairah                  |
| Strongest spread         | Fujairah vs Rotterdam     |
| Best route alternative   | Rotterdam before Fujairah |
| Second route alternative | Gibraltar before Fujairah |

The analysis shows that Rotterdam was consistently the most attractive port in the selected sample, while Fujairah was the most expensive. The largest theoretical savings appeared when comparing Fujairah against Rotterdam.

After applying simplified operational assumptions, both Rotterdam and Gibraltar remained profitable alternatives in the Europe to Fujairah route scenario.

---

# 9. Final Summary

This project develops a complete analytical pipeline to study VLSFO bunker fuel price differences across major global ports and evaluate whether those differences can support route-based arbitrage decisions.

The first part of the project focuses on data collection, cleaning and exploratory analysis. Recent public bunker price data is transformed into a structured dataset, allowing ports to be compared by average price, daily ranking, price range and volatility.

The analysis shows a clear price hierarchy among the selected ports. Rotterdam is the cheapest port on average, Gibraltar is the second cheapest, and Fujairah is the most expensive and most volatile. This creates strong theoretical spreads, especially between Fujairah and Rotterdam.

The second part of the project moves from simple price comparison to route-based decision-making. By comparing the cost of buying VLSFO earlier in Rotterdam or Gibraltar against buying later in Fujairah, the model estimates potential gross and net savings for a Europe to Fujairah route.

The results show that both Rotterdam and Gibraltar remain profitable alternatives under the simplified assumptions used in the model. Rotterdam provides the strongest savings because of its lower VLSFO price level.

Overall, the project shows that bunker fuel price analysis becomes more valuable when it is connected to routes, vessel characteristics and commercial decision-making. The cheapest port is only useful if it fits the vessel’s route, timing and fuel capacity constraints.

---

# Limitations

This is a portfolio version of the model. The main limitations are:

* Free public bunker price data provides only limited recent history.
* Full historical port-level bunker price data is usually paid market data.
* Operational costs are simplified assumptions.
* Vessel fuel consumption is based on simplified vessel profiles.
* The model does not include weather, congestion, AIS data or supplier-specific availability.
* The analysis focuses only on VLSFO.
* The route model is simplified and should not be used as a real trading or procurement tool without further validation.

---

# Future Improvements

The project could be improved by adding:

* more ports and routes
* MGO and HSFO analysis
* real port call cost estimates
* vessel-specific consumption curves
* AIS-based route data
* congestion and waiting time data
* paid historical bunker market data
* Power BI dashboard visualisations
* scenario analysis for different vessel types and bunker quantities

---

# Author

Antonio Espino Bautista

Economics & Business Intelligence
Marine Fuel Analytics | Bunkering | Route Optimisation | Trading

GitHub:
https://github.com/antespbau
