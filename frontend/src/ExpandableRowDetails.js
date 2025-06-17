import React from 'react'
import { Table, TableBody, TableCell, TableRow, TableHead } from '@mui/material'

function ExpandableRowDetails ({ pair }) {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell />
          <TableCell>Average Odds</TableCell>
          <TableCell>Best Odds</TableCell>
          <TableCell>+EV%</TableCell>
          <TableCell>Bet MGM</TableCell>
          <TableCell>Bet Rivers</TableCell>
          <TableCell>Draft Kings</TableCell>
          <TableCell>Fan Duel</TableCell>
          <TableCell>Caesars</TableCell>
          <TableCell>ESPN Bet</TableCell>
          <TableCell>BetFred</TableCell>
          <TableCell>SuperBook</TableCell>
          <TableCell>HardRock</TableCell>
          <TableCell>BET PARX</TableCell>
          <TableCell>Tipico</TableCell>
          <TableCell>Bovada</TableCell>
          <TableCell>Pinnacle</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {pair.bets.map((bet, index) => (
          <TableRow key={index}>
            <TableCell>
              {bet.description + ' ' + bet.outcome + ' ' + bet.point}
            </TableCell>
            <TableCell>{bet.average_odds}</TableCell>
            <TableCell>{bet.best_ev_odds}</TableCell>
            <TableCell>{(bet.best_ev * 100).toFixed(2)}%</TableCell>
            <TableCell>{bet.betmgm_odds}</TableCell>
            <TableCell>{bet.betrivers_odds}</TableCell>
            <TableCell>{bet.draftkings_odds}</TableCell>
            <TableCell>{bet.fanduel_odds}</TableCell>
            <TableCell>{bet.williamhill_us_odds}</TableCell>
            <TableCell>{bet.espnbet_odds}</TableCell>
            <TableCell>{bet.windcreek_odds}</TableCell>
            <TableCell>{bet.superbook_odds}</TableCell>
            <TableCell>{bet.hardrockbet_odds}</TableCell>
            <TableCell>{bet.betparx_odds}</TableCell>
            <TableCell>{bet.tipico_us_odds}</TableCell>
            <TableCell>{bet.bovada_odds}</TableCell>
            <TableCell>{bet.pinnacle_odds}</TableCell>
            {/* Add more cells as needed */}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default ExpandableRowDetails
