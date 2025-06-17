import React, { useState } from 'react'
import axios from 'axios'
import {
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  IconButton,
  Button,
  Collapse,
  TextField,
  Checkbox,
  FormControlLabel
} from '@mui/material'
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown'
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'
import ExpandableRowDetails from './ExpandableRowDetails'

function DataTable () {
  const [data, setData] = useState([])
  const [open, setOpen] = useState({})
  const [checkedState, setCheckedState] = useState({})
  const [sortConfig, setSortConfig] = useState({
    key: 'best_ev',
    direction: 'descending'
  })

  // Want to see if this is picked up!

  const bookmakerOptions = [
    { key: 'betmgm', displayName: 'Bet MGM' },
    { key: 'betrivers', displayName: 'Bet Rivers' },
    { key: 'draftkings', displayName: 'Draft Kings' },
    { key: 'fanduel', displayName: 'Fan Duel' },
    { key: 'williamhill_us', displayName: 'Caesars' },
    { key: 'espnbet', displayName: 'ESPN Bet' },
    { key: 'windcreek', displayName: 'Bet Fred' },
    { key: 'superbook', displayName: 'SuperBook' },
    { key: 'hardrockbet', displayName: 'HardRock' },
    { key: 'betparx', displayName: 'BET PARX' },
    { key: 'tipico_us', displayName: 'Tipico' },
    { key: 'pinnacle', displayName: 'Pinnacle' },
    { key: 'bovada', displayName: 'Bovada' }
  ]

  const [inputs, setInputs] = useState({
    // sport: '',
    bankroll: 1000,
    kelly_fraction: 0.25,
    max_odds: 3,
    // Simulated list of bookmakers
    bookmakers: bookmakerOptions.reduce(
      (acc, { key }) => ({ ...acc, [key]: true }),
      {}
    )
  })

  const fetchData = async () => {
    try {
      // const csrfToken = getCsrfToken()
      // Update the URL and data payload according to your API requirements
      // const response = await axios.post('/pev_app/get_posts/', inputs)
      const response = await axios.post('/pev_app/fetch_data/', inputs)
      // const response = await axios.get('/pev_app/fetch_data/')
      const jsonData = JSON.parse(response.data)

      console.log(jsonData)

      const sortedData = jsonData
        .map(pair => {
          const bestPositiveEvBet = pair.bets.reduce((best, bet) => {
            return bet.best_ev > 0 && bet.best_ev > (best.best_ev || 0)
              ? bet
              : best
          }, {})
          return { ...pair, bestPositiveEvBet }
        })
        .sort((a, b) =>
          sortConfig.direction === 'ascending'
            ? a.bestPositiveEvBet.best_ev - b.bestPositiveEvBet.best_ev
            : b.bestPositiveEvBet.best_ev - a.bestPositiveEvBet.best_ev
        )

      setData(sortedData)
    } catch (error) {
      console.error('Error fetching data:', error)
      setData([])
    }
  }

  const handleChange = event => {
    const { name, value } = event.target
    setInputs(prev => ({ ...prev, [name]: value }))
  }

  const handleBookmakerCheckChange = event => {
    const { name, checked } = event.target
    setInputs(prev => ({
      ...prev,
      bookmakers: {
        ...prev.bookmakers,
        [name]: checked
      }
    }))
  }

  const handleCheckboxChange = (pair, isChecked) => {
    setCheckedState(prev => ({ ...prev, [pair.pair_id]: isChecked }))
    if (isChecked === true) {
      handleSaveBet(pair)
    }
  }

  const handleRowClick = pairId => {
    setOpen(prevOpen => ({ ...prevOpen, [pairId]: !prevOpen[pairId] }))
  }

  const requestSort = key => {
    const direction =
      sortConfig.key === key && sortConfig.direction === 'ascending'
        ? 'descending'
        : 'ascending'
    setSortConfig({ key, direction })
    const sortedData = [...data].sort((a, b) => {
      const valueA = a.bestPositiveEvBet[key]
      const valueB = b.bestPositiveEvBet[key]
      if (typeof valueA === 'string') {
        return direction === 'ascending'
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA)
      }
      return direction === 'ascending' ? valueA - valueB : valueB - valueA
    })
    setData(sortedData)
  }

  const sortIndicator = columnName => {
    return sortConfig.key === columnName ? (
      sortConfig.direction === 'ascending' ? (
        <ArrowUpwardIcon fontSize='small' />
      ) : (
        <ArrowDownwardIcon fontSize='small' />
      )
    ) : null
  }

  const handleSaveBet = async pair => {
    console.log('Saving bet for pair:', pair, pair.bestPositiveEvBet.p_key)
    try {
      await axios.post('/pev_app/save_bet/', {
        pair: pair,
        p_key: pair.bestPositiveEvBet.p_key
      })
    } catch (error) {
      console.error('Error saving bet:', error)
    }
  }

  return (
    <div>
      <TextField
        label='Bankroll'
        name='bankroll'
        type='number'
        value={inputs.bankroll}
        onChange={handleChange}
      />
      <TextField
        label='Kelly Fraction'
        name='kelly_fraction'
        type='number'
        value={inputs.kelly_fraction}
        onChange={handleChange}
      />
      <TextField
        label='Max Odds'
        name='max_odds'
        type='number'
        value={inputs.max_odds}
        onChange={handleChange}
      />
      <div>
        {bookmakerOptions.map(({ key, displayName }) => (
          <FormControlLabel
            key={key}
            control={
              <Checkbox
                checked={inputs.bookmakers[key]}
                onChange={handleBookmakerCheckChange}
                name={key}
              />
            }
            label={displayName}
          />
        ))}
      </div>

      <Button onClick={fetchData} variant='contained' color='primary'>
        Fetch Data
      </Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell />
              <TableCell>Save Bet</TableCell>
              <TableCell onClick={() => requestSort('best_ev')}>
                +EV% {sortIndicator('best_ev')}
              </TableCell>
              <TableCell onClick={() => requestSort('sport')}>
                Sport {sortIndicator('sport')}
              </TableCell>
              <TableCell onClick={() => requestSort('description')}>
                Option {sortIndicator('description')}
              </TableCell>
              <TableCell onClick={() => requestSort('market')}>
                Market {sortIndicator('market')}
              </TableCell>
              <TableCell onClick={() => requestSort('event')}>
                Event {sortIndicator('event')}
              </TableCell>
              <TableCell onClick={() => requestSort('outcome')}>
                Side {sortIndicator('outcome')}
              </TableCell>
              <TableCell onClick={() => requestSort('point')}>
                Point {sortIndicator('point')}
              </TableCell>
              <TableCell onClick={() => requestSort('average_odds')}>
                Average Odds {sortIndicator('average_odds')}
              </TableCell>
              <TableCell onClick={() => requestSort('best_ev_odds')}>
                Best Odds {sortIndicator('best_ev_odds')}
              </TableCell>
              <TableCell onClick={() => requestSort('best_ev_bookmaker')}>
                Best Odds Bookmaker {sortIndicator('best_ev_bookmaker')}
              </TableCell>
              <TableCell onClick={() => requestSort('bet_amount')}>
                Bet Amount {sortIndicator('bet_amount')}
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((pair, index) => (
              <React.Fragment key={index}>
                <TableRow>
                  <TableCell onClick={() => handleRowClick(pair.pair_id)}>
                    <IconButton size='small'>
                      {open[pair.pair_id] ? (
                        <KeyboardArrowUpIcon />
                      ) : (
                        <KeyboardArrowDownIcon />
                      )}
                    </IconButton>
                  </TableCell>
                  <TableCell>
                    {/* <Checkbox onChange={() => handleSaveBet(pair)} /> */}
                    <Checkbox
                      checked={!!checkedState[pair.pair_id]}
                      onChange={e =>
                        handleCheckboxChange(pair, e.target.checked)
                      }
                    />
                  </TableCell>
                  <TableCell>
                    {(pair.bestPositiveEvBet.best_ev * 100).toFixed(2)}%
                  </TableCell>
                  <TableCell>{pair.bestPositiveEvBet.sport_title}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.description}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.market}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.event}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.outcome}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.point}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.average_odds}</TableCell>
                  <TableCell>{pair.bestPositiveEvBet.best_ev_odds}</TableCell>
                  <TableCell>
                    {pair.bestPositiveEvBet.best_ev_bookmaker}
                  </TableCell>
                  <TableCell>${pair.bestPositiveEvBet.bet_amount}</TableCell>
                  {/* <TableCell>
                    <Checkbox onChange={() => handleSaveBet(pair)} />
                  </TableCell> */}
                  {/* <TableCell>
                    <Checkbox
                      checked={!!checkedState[pair.pair_id]}
                      onChange={e =>
                        handleCheckboxChange(pair, e.target.checked)
                      }
                    />
                  </TableCell> */}
                </TableRow>
                <TableRow>
                  <TableCell
                    style={{ paddingBottom: 0, paddingTop: 0 }}
                    colSpan={12}
                  >
                    <Collapse
                      in={open[pair.pair_id]}
                      timeout='auto'
                      unmountOnExit
                    >
                      <ExpandableRowDetails pair={pair} />
                    </Collapse>
                  </TableCell>
                </TableRow>
              </React.Fragment>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}

export default DataTable
