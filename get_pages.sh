# The site has a pagination limit of 10000 items.
# To overcome this limit, navigate the default scroll in ascending 
# and descending order. Finally, remove the douplicate and voila!

# Constants
START_PAGE=1
END_PAGE=600  # Maximum allowed size (aprox.)
N=16  # Maximum number of process in parallel
LANG="es"
ORDER="asc"  # asc / desc
BASE_PATH=pages/$ORDER

# Parallel task
download_page () {
  local i=$1
  local century=$2
  local filename=$3
  echo "Downloading page #$i... (from: $century))"

  curl 'https://resultados4.museodelprado.es/CargadorResultados/CargarResultados' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: https://www.museodelprado.es' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://www.museodelprado.es/' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  --data-raw "pUsarMasterParaLectura=false&pProyectoID=7317a29a-d846-4c54-9034-6a114c3658fe&pEsUsuarioInvitado=true&pIdentidadID=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF&pParametros=ecidoc%3Ap62_E52_p79_has_time-span_beginning%3D$century%7Cpagina%3D$i&pLanguageCode=$LANG&pPrimeraCarga=false&pAdministradorVeTodasPersonas=false&pTipoBusqueda=0&pNumeroParteResultados=1&pGrafo=7317a29a-d846-4c54-9034-6a114c3658fe&pFiltroContexto=&pParametros_adiccionales=PestanyaActualID%3Dc89fbb0c-a52c-4700-9220-79f4964d3949%7Crdf%3Atype%3Dpmartwork%7Corden%3D$ORDER%7CordenarPor%3Dpm%3Arelevance%2Cecidoc%3Ap62_E52_p79_has_time-span_beginning%2Cecidoc%3Ap62_E52_p80_has_time-span_end%2Cgnoss%3Ahasfechapublicacion&cont=5" \
  --compressed \
  --insecure > $filename

#  sleep 0.5  # Wait n seconds
}


# Useless! Waste of time (asc+desc was easier)
# Declare century array to split works (to overcome the "10000 LIMIT" problem)
declare -a c_array=("")#(-2100000--2000000 -5000000--4000000 -4000000--3000000 -3000000--2000000 -1000000-0000000 0000000-1000000 1000000-2000000 2000000-3000000 3000000-4000000 5000000-6000000 11000000-12000000 12000000-13000000 13000000-14000000 14000000-15000000 15000000-16000000 16000000-17000000 17000000-18000000 18000000-19000000 19000000-20000000)

for cent in "${c_array[@]}"; do

  # Create pages path if doesn't exists
  PAGES_PATH="$BASE_PATH/$cent"
  if [ ! -d "$PAGES_PATH" ]; then
    mkdir -p "$PAGES_PATH"
  else
    echo "Skip folder."
  fi

  # Launch tasks
  for i in $(seq $START_PAGE $END_PAGE); do
    # Check if file exists
    PAGE_FILE="$PAGES_PATH/page-$ORDER-$i.json"
    if [ ! -f  $PAGE_FILE ]; then
      download_page "$i" "$cent" "$PAGE_FILE" &  # Fork process (parallel)
      ((counter=i%N)); ((counter++==0)) && wait  # Wait for N parallel processes to finish
    else
      echo "Skip page #$i. File exists."
    fi
  done
done

echo "Done!"