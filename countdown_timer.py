import os
from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


app = Dash(__name__
         , external_stylesheets = [dbc.themes.DARKLY]
         , prevent_initial_callbacks = True
          )
countdown_store = dcc.Store(id = "countdown-store")
running_countdown_store = dcc.Store(id = "running-countdown-store")
interval = dcc.Interval(id = "countdown-interval"
                      , interval = 1000 # IN MILLISECONDS
                      , n_intervals = 0
                       )
countdown_input = dcc.Input(
                            id = "countdown-input"
                          , type = "number"
                          , min = 0
                          , step = 1
                          , size = "lg"
                          , style = {"font-size": "1.6rem"}
                          , className = "mb-3"
                           )
button = dbc.Button(
                    id = "countdown-button"
                  , children = "Start Countdown"
                  , n_clicks = 0
                  , size = "lg"
                  , style = {"font-size": "1.6rem"}
                  , color = "secondary"
                  , className = "me-1"
                   )

led_display = daq.LEDDisplay(
                             id = "countdown-display"
                           , value = "00:00:00:00:00:00:00:00"
                           , label = {
                                    "label": "Time in century : decades : years : months : days : hours : minutes : seconds"
                                  , "style": {"font-size": "1.6rem", "text-align": "center"}
                                   }
                           , backgroundColor = "black"
                           , color = "skyblue"
                           , labelPosition = "bottom"
                           , size = 75
                            )
audio_div = html.Div(id = "audio-div")
app.layout = dbc.Container(
    [
          countdown_store
        , running_countdown_store
        , interval
        , audio_div
        , dbc.Row(
                    [
                        dbc.Col(
                                [
                                 html.H2("JayRizzo's Countdown From Seconds")
                               , countdown_input
                                ]
                              , lg = 6
                               )
                    ]
                , justify = "center"
                , style = dict(textAlign = "center")
                , className = "d-flex justify-content-center"
                 )
        , dbc.Row([dbc.Col([button], lg = 6, style = dict(textAlign = "center"))], justify = "center", className = "mt-4")
        , dbc.Row([dbc.Col([led_display], lg = 6, style = dict(textAlign = "center"))], justify = "center", className = "mt-4")
    ]
    , className = "p-4"
    , fluid = True
)


@app.callback(
              Output("countdown-store", "data")
            , Output("countdown-interval", "n_intervals")
            , Input("countdown-button", "n_clicks")
            , State("countdown-input", "value")
             )


def init_countdown_store(n_clicks, countdown_input):
    if n_clicks > 0:
        return countdown_input, 0


@app.callback(
              Output("running-countdown-store", "data")
            , Input("countdown-store", "data")
            , Input("countdown-interval", "n_intervals")
             )


def init_running_countdown_store(seconds, n_intervals):
    if seconds is not None:
        running_seconds = seconds - n_intervals
        if running_seconds >= 0:
            return running_seconds
        else:
            return 0


@app.callback(
    Output("countdown-display", "value")
         , Output("countdown-display", "label")
         , Output("audio-div", "children")
         , Input("running-countdown-store", "data")
          )


def update_countdown_display(seconds):
    audio = html.Div()
    if seconds is not None:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        months, days = divmod(days, 30)
        years, months = divmod(months, 12)
        decades, years = divmod(years, 10)
        century, decades = divmod(decades, 10)
        label_str = (
              is_non_zero(seconds)  * "Time Left in "
            + is_non_zero(century)  * f"\n{century} : centuries "
            + is_non_zero(decades)  * f"\n{decades} : decades "
            + is_non_zero(years)    * f"\n{years} : years "
            + is_non_zero(months)   * f"\n{months} : months "
            + is_non_zero(days)     * f"\n{days} : days "
            + is_non_zero(hours)    * f"\n{hours} : hours "
            + is_non_zero(mins)     * f"\n{mins} : minutes "
            + is_non_zero(secs)     * f"\n{secs} : seconds "
      )
        try:
            if seconds == 0 and mins == 0 and hours == 0 and days == 0 and months == 0 and years == 0 and decades == 0 and century == 0:
                audio = html.Audio(
                    src = "/System/Library/Sounds/Sosumi.aiff", controls = False, autoPlay = True
                    # src = "./assets/clock-alarm-8761.mp3", controls = False, autoPlay = True
                )
                os.system('afplay /System/Library/Sounds/Sosumi.aiff')
        except Exception as e:
            print(f"{Exception} :: {e}")
        return (
                f"{century:02d}:{decades:02d}:{years:02d}:{months:02d}:{days:02d}:{hours:02d}:{mins:02d}:{secs:02d}"
              , {
                 "label": label_str
               , "style": {"font-size": "1.5rem", "text-align": "right"}
                }
              , audio
               )
    else:
        return (
                "00:00:00:00:00:00:00"
              , {
                 "label": f"Time in centuries : decades : years : months : days : hours : minutes : seconds "
               , "style": {"font-size": "1.5rem", "text-align": "right"}
                }
              , audio
              ,
               )


def is_non_zero(number):
    x = {True: 1, False: 0}[number != 0]
    return x


if __name__ == "__main__":
    app.run_server(debug = True, port = 8090)
