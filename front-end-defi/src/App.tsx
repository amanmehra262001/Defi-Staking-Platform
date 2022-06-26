import { DAppProvider, ChainId } from "@usedapp/core"
import { Header } from "./components/Headers"
import { Main } from "./components/Main"
import { Container } from "@material-ui/core"
import React from 'react'

function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Kovan],
      notifications: {
        expirationPeriod: 1000,
        checkInterval: 1000
      }
    }}>
      <Header />
      <Container maxWidth="md">
        <Main />
      </Container>
    </DAppProvider>
  )
}

export default App
