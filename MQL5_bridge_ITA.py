import streamlit as st
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import time

# Configurazione pagina
st.set_page_config(page_title="mt5 Trading App - Filtered", layout="wide")

# Inizializza session state all'inizio
if 'connected' not in st.session_state:
    st.session_state['connected'] = False
if 'account_info' not in st.session_state:
    st.session_state['account_info'] = None
if 'filter_comment' not in st.session_state:
    st.session_state['filter_comment'] = "Streamlit Trade"

st.title("📈 MT5 Trading Application - Con Filtro Commento")
st.markdown("---")

# Sidebar per configurazione account
with st.sidebar:
    st.header("⚙️ Configurazione Account mt5")

    account_number = st.number_input("Numero Conto", min_value=0, value=0, step=1)
    password = st.text_input("Password", type="password")
    server = st.text_input("Server", value="")

    st.markdown("---")

    if st.button("🔌 Connetti a MT5", use_container_width=True):
        if not mt5.initialize():
            st.error(f"❌ Inizializzazione MT5 fallita: {mt5.last_error()}")
            st.session_state['connected'] = False
        else:
            authorized = mt5.login(account_number, password=password, server=server)
            if authorized:
                st.success("✅ Connessione riuscita!")
                st.session_state['connected'] = True
                account_info = mt5.account_info()
                if account_info:
                    st.session_state['account_info'] = account_info
                    st.info(f"💰 Balance: {account_info.balance} {account_info.currency}")
                    st.info(f"📊 Equity: {account_info.equity} {account_info.currency}")
            else:
                st.error(f"❌ Login fallito: {mt5.last_error()}")
                st.session_state['connected'] = False
                st.session_state['account_info'] = None

    if st.button("🔌 Disconnetti", use_container_width=True):
        mt5.shutdown()
        st.session_state['connected'] = False
        st.session_state['account_info'] = None
        st.info("Disconnesso da mt5")

    # Mostra stato connessione
    st.markdown("---")
    if st.session_state['connected']:
        st.success("🟢 Connesso")
    else:
        st.warning("🔴 Non connesso")

# Main area - Trading interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💹 Pannello Trading")

    # Input parametri trade
    symbol = st.text_input("Simbolo", value="EURUSD", help="Inserisci il simbolo da tradare (es: EURUSD, GBPUSD)")

    col_size, col_sl, col_tp = st.columns(3)

    with col_size:
        lot_size = st.number_input("Size (Lotti)", min_value=0.01, value=0.1, step=0.01, format="%.2f")

    with col_sl:
        stop_loss = st.number_input("Stop Loss (pips)", min_value=0, value=0, step=1)

    with col_tp:
        take_profit = st.number_input("Take Profit (pips)", min_value=0, value=0, step=1)

    comment = st.text_input("Commento (per identificare i trade)", value="Streamlit Trade",
                            help="Inserisci un commento univoco per filtrare solo i trade di questa app")

    # Salva il commento nel session state per il filtro
    if comment:
        st.session_state['filter_comment'] = comment

    st.markdown("---")

    # Pulsanti BUY e SELL
    col_buy, col_sell = st.columns(2)

    with col_buy:
        if st.button("🟢 BUY", use_container_width=True, type="primary"):
            if not st.session_state.get('connected', False):
                st.error("❌ Non sei connesso a mt5! Connettiti dalla sidebar.")
            else:
                with st.spinner("Invio ordine BUY..."):
                    try:
                        # Prepara la richiesta di trade
                        symbol_info = mt5.symbol_info(symbol)
                        if symbol_info is None:
                            st.error(f"❌ Simbolo {symbol} non trovato")
                        else:
                            if not symbol_info.visible:
                                if not mt5.symbol_select(symbol, True):
                                    st.error(f"❌ Impossibile selezionare il simbolo {symbol}")
                                    st.stop()

                            point = symbol_info.point
                            price = mt5.symbol_info_tick(symbol).ask

                            # Calcola SL e TP
                            sl = price - stop_loss * point * 10 if stop_loss > 0 else 0
                            tp = price + take_profit * point * 10 if take_profit > 0 else 0

                            request = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": symbol,
                                "volume": lot_size,
                                "type": mt5.ORDER_TYPE_BUY,
                                "price": price,
                                "sl": sl,
                                "tp": tp,
                                "deviation": 20,
                                "magic": 234000,
                                "comment": comment,
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC,
                            }

                            # Invia ordine
                            result = mt5.order_send(request)

                            if result is None:
                                st.error(f"❌ Ordine BUY fallito: {mt5.last_error()}")
                            elif result.retcode != mt5.TRADE_RETCODE_DONE:
                                st.error(f"❌ Ordine BUY fallito: {result.retcode} - {result.comment}")
                            else:
                                st.success(f"✅ Ordine BUY eseguito con successo!")
                                st.balloons()
                                st.info(f"🎫 Ticket: {result.order}")
                                st.info(f"💰 Volume: {result.volume} lotti")
                                st.info(f"💵 Prezzo: {result.price}")
                    except Exception as e:
                        st.error(f"❌ Errore: {str(e)}")

    with col_sell:
        if st.button("🔴 SELL", use_container_width=True, type="secondary"):
            if not st.session_state.get('connected', False):
                st.error("❌ Non sei connesso a mt5! Connettiti dalla sidebar.")
            else:
                with st.spinner("Invio ordine SELL..."):
                    try:
                        # Prepara la richiesta di trade
                        symbol_info = mt5.symbol_info(symbol)
                        if symbol_info is None:
                            st.error(f"❌ Simbolo {symbol} non trovato")
                        else:
                            if not symbol_info.visible:
                                if not mt5.symbol_select(symbol, True):
                                    st.error(f"❌ Impossibile selezionare il simbolo {symbol}")
                                    st.stop()

                            point = symbol_info.point
                            price = mt5.symbol_info_tick(symbol).bid

                            # Calcola SL e TP
                            sl = price + stop_loss * point * 10 if stop_loss > 0 else 0
                            tp = price - take_profit * point * 10 if take_profit > 0 else 0

                            request = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": symbol,
                                "volume": lot_size,
                                "type": mt5.ORDER_TYPE_SELL,
                                "price": price,
                                "sl": sl,
                                "tp": tp,
                                "deviation": 20,
                                "magic": 234000,
                                "comment": comment,
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC,
                            }

                            # Invia ordine
                            result = mt5.order_send(request)

                            if result is None:
                                st.error(f"❌ Ordine SELL fallito: {mt5.last_error()}")
                            elif result.retcode != mt5.TRADE_RETCODE_DONE:
                                st.error(f"❌ Ordine SELL fallito: {result.retcode} - {result.comment}")
                            else:
                                st.success(f"✅ Ordine SELL eseguito con successo!")
                                st.balloons()
                                st.info(f"🎫 Ticket: {result.order}")
                                st.info(f"💰 Volume: {result.volume} lotti")
                                st.info(f"💵 Prezzo: {result.price}")
                    except Exception as e:
                        st.error(f"❌ Errore: {str(e)}")

with col2:
    st.header("📊 Posizioni Aperte")

    # FILTRO PER COMMENTO
    st.markdown("#### 🔍 Filtro Visualizzazione")
    filter_enabled = st.checkbox("Mostra solo posizioni con commento specifico", value=False)

    if filter_enabled:
        filter_comment_input = st.text_input(
            "Commento da filtrare",
            value=st.session_state.get('filter_comment', 'Streamlit Trade'),
            help="Visualizza solo le posizioni con questo commento"
        )
        st.info(f"🔎 Filtro attivo: '{filter_comment_input}'")
    else:
        filter_comment_input = None
        st.info("📋 Mostro tutte le posizioni")

    st.markdown("---")

    # AUTO-REFRESH
    col_refresh1, col_refresh2 = st.columns([1, 1])

    with col_refresh1:
        auto_refresh = st.checkbox("🔄 Aggiornamento Automatico", value=False)

    with col_refresh2:
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Intervallo (secondi)",
                options=[1, 2, 3, 5, 10, 30],
                index=2,  # default 3 secondi
                key="refresh_interval"
            )
        else:
            refresh_interval = 5

    if auto_refresh:
        st.info(f"⏱️ Aggiornamento ogni {refresh_interval} secondi")
        import time

        time.sleep(refresh_interval)
        st.rerun()

    if st.button("🔄 Aggiorna Manualmente", use_container_width=True):
        st.rerun()

    if st.session_state.get('connected', False):
        try:
            # Recupera tutte le posizioni
            all_positions = mt5.positions_get()

            if all_positions is None or len(all_positions) == 0:
                st.info("Nessuna posizione aperta")
            else:
                # Filtra le posizioni se il filtro è attivo
                if filter_enabled and filter_comment_input:
                    filtered_positions = [pos for pos in all_positions if pos.comment == filter_comment_input]
                else:
                    filtered_positions = list(all_positions)

                # Mostra statistiche
                total_positions = len(all_positions)
                filtered_count = len(filtered_positions)

                if filter_enabled and filter_comment_input:
                    st.caption(f"Posizioni filtrate: {filtered_count} / {total_positions} totali")
                else:
                    st.caption(f"Posizioni totali: {total_positions}")

                if len(filtered_positions) == 0:
                    if filter_enabled:
                        st.warning(f"⚠️ Nessuna posizione trovata con commento '{filter_comment_input}'")
                    else:
                        st.info("Nessuna posizione aperta")
                else:
                    # Calcola profit totale delle posizioni filtrate
                    total_profit = sum([pos.profit for pos in filtered_positions])
                    profit_color = "🟢" if total_profit >= 0 else "🔴"
                    st.metric("Profit Totale (filtrato)", f"{profit_color} {total_profit:.2f}")

                    # Pulsante per chiudere TUTTE le posizioni filtrate
                    if len(filtered_positions) > 1:
                        st.markdown("---")
                        if st.button(f"⚠️ CHIUDI TUTTE LE {len(filtered_positions)} POSIZIONI",
                                     type="primary",
                                     use_container_width=True,
                                     key="close_all"):
                            with st.spinner(f"Chiusura di {len(filtered_positions)} posizioni..."):
                                closed_count = 0
                                failed_count = 0

                                for pos in filtered_positions:
                                    try:
                                        close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
                                        tick = mt5.symbol_info_tick(pos.symbol)

                                        if tick is None:
                                            failed_count += 1
                                            continue

                                        close_price = tick.bid if pos.type == 0 else tick.ask

                                        close_request = {
                                            "action": mt5.TRADE_ACTION_DEAL,
                                            "symbol": pos.symbol,
                                            "volume": pos.volume,
                                            "type": close_type,
                                            "position": pos.ticket,
                                            "price": close_price,
                                            "deviation": 20,
                                            "magic": 234000,
                                            "comment": f"Close All {pos.ticket}",
                                            "type_time": mt5.ORDER_TIME_GTC,
                                            "type_filling": mt5.ORDER_FILLING_IOC,
                                        }

                                        result = mt5.order_send(close_request)

                                        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
                                            closed_count += 1
                                        else:
                                            failed_count += 1

                                    except Exception:
                                        failed_count += 1

                                if closed_count > 0:
                                    st.success(f"✅ {closed_count} posizioni chiuse con successo!")
                                if failed_count > 0:
                                    st.warning(f"⚠️ {failed_count} posizioni non chiuse")

                                st.balloons()
                                time.sleep(1)
                                st.rerun()

                    st.markdown("---")

                    # Mostra le posizioni filtrate
                    for pos in filtered_positions:
                        with st.expander(f"#{pos.ticket} - {pos.symbol} {'🟢' if pos.profit >= 0 else '🔴'}"):
                            col_info1, col_info2 = st.columns(2)

                            with col_info1:
                                st.write(f"**Tipo:** {'BUY' if pos.type == 0 else 'SELL'}")
                                st.write(f"**Volume:** {pos.volume} lotti")
                                st.write(f"**Prezzo apertura:** {pos.price_open}")
                                st.write(f"**Prezzo corrente:** {pos.price_current}")

                            with col_info2:
                                profit_color = "🟢" if pos.profit >= 0 else "🔴"
                                st.write(f"**Profit:** {profit_color} {pos.profit:.2f}")
                                st.write(f"**SL:** {pos.sl if pos.sl > 0 else 'N/A'}")
                                st.write(f"**TP:** {pos.tp if pos.tp > 0 else 'N/A'}")
                                st.write(f"**Commento:** {pos.comment}")

                            st.markdown("---")

                            # Pulsante per chiudere la posizione
                            if st.button(f"❌ Chiudi Posizione #{pos.ticket}", key=f"close_{pos.ticket}",
                                         type="secondary", use_container_width=True):
                                with st.spinner(f"Chiusura posizione #{pos.ticket}..."):
                                    try:
                                        # Determina il tipo di chiusura (opposto al tipo di apertura)
                                        close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY

                                        # Ottieni il prezzo corrente
                                        tick = mt5.symbol_info_tick(pos.symbol)
                                        if tick is None:
                                            st.error(f"❌ Impossibile ottenere il prezzo per {pos.symbol}")
                                        else:
                                            close_price = tick.bid if pos.type == 0 else tick.ask

                                            # Crea la richiesta di chiusura
                                            close_request = {
                                                "action": mt5.TRADE_ACTION_DEAL,
                                                "symbol": pos.symbol,
                                                "volume": pos.volume,
                                                "type": close_type,
                                                "position": pos.ticket,
                                                "price": close_price,
                                                "deviation": 20,
                                                "magic": 234000,
                                                "comment": f"Close {pos.ticket}",
                                                "type_time": mt5.ORDER_TIME_GTC,
                                                "type_filling": mt5.ORDER_FILLING_IOC,
                                            }

                                            # Invia la richiesta di chiusura
                                            result = mt5.order_send(close_request)

                                            if result is None:
                                                st.error(f"❌ Chiusura fallita: {mt5.last_error()}")
                                            elif result.retcode != mt5.TRADE_RETCODE_DONE:
                                                st.error(f"❌ Chiusura fallita: {result.retcode} - {result.comment}")
                                            else:
                                                st.success(f"✅ Posizione #{pos.ticket} chiusa con successo!")
                                                st.info(f"💰 Profit finale: {pos.profit:.2f}")
                                                st.balloons()
                                                time.sleep(1)
                                                st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Errore nella chiusura: {str(e)}")

        except Exception as e:
            st.error(f"Errore nel recupero delle posizioni: {str(e)}")
    else:
        st.warning("⚠️ Connettiti a mt5 per vedere le posizioni")

# Footer
st.markdown("---")
st.caption("⚠️ ATTENZIONE: Questa è un'applicazione di trading reale. Usa con cautela!")
st.caption("💡 TIP: Usa commenti univoci per identificare i trade di questa applicazione e filtrarli facilmente!")
