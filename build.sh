#!/bin/bash

registry=${1:-wesparish}
imagename=${2:-$(basename $PWD)}

privateRegistry=${3:-}

buildDate=$(date +%Y-%m-%d-%H%M%S)

set -e

for dockerfile in $(find  -name Dockerfile); do
  rsync -av --delete ./crypto-prometheus/ $(dirname $dockerfile)/crypto-prometheus/
  versionvariant=$(dirname $dockerfile | sed -e 's|^./||g' -e 's|/|-|g')
  echo Building variant: $versionvariant
  echo docker build -t $registry/${imagename}:${versionvariant} $(dirname $dockerfile)
  docker build -t $registry/${imagename}:$versionvariant $(dirname $dockerfile)
  echo docker push $registry/${imagename}:${versionvariant}
  docker push $registry/${imagename}:$versionvariant

  docker tag $registry/${imagename}:${versionvariant} $registry/${imagename}:${versionvariant}-${buildDate}
  echo docker push $registry/${imagename}:${versionvariant}-${buildDate}
  docker push $registry/${imagename}:${versionvariant}-${buildDate}

  if [ -n "$privateRegistry" ] ; then
    echo docker tag $registry/${imagename}:${versionvariant} ${privateRegistry}/${imagename}:${versionvariant}
    docker tag $registry/${imagename}:$versionvariant ${privateRegistry}/${imagename}:$versionvariant
    echo docker push ${privateRegistry}/${imagename}:${versionvariant}
    docker push ${privateRegistry}/${imagename}:$versionvariant

    docker tag $registry/${imagename}:${versionvariant} $registry/${imagename}:${versionvariant}-${buildDate}
    echo docker push $registry/${imagename}:${versionvariant}-${buildDate}
    docker push $registry/${imagename}:${versionvariant}-${buildDate}
  fi
done

set +e
